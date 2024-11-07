import ibis
import pandas as pd
from typing import List, Dict, Any

def check_ambig_table_name(tbl_name: str, mdc: pd.DataFrame) -> None:
    schemas = mdc[mdc['table_name'] == 'capture']['table_schema'].unique()
    if len(schemas) > 1:
        raise ValueError(f"Multiple tables named '{tbl_name}' found, in schemas: {', '.join(schemas)}.\n\tResults are ambiguous. Try filtering metadata_columns to the schema of interest.")

def tbl_pkey(tbl_name: str, metadata_columns: pd.DataFrame) -> List[str]:
    check_ambig_table_name(tbl_name, metadata_columns)
    return metadata_columns[(metadata_columns['table_name'] == tbl_name) & 
                            (metadata_columns['key_type'].isin(['PK', 'PF']))]['column_name'].tolist()

def tbl_fkey(tbl_name: str, metadata_columns: pd.DataFrame) -> List[str]:
    check_ambig_table_name(tbl_name, metadata_columns)
    return metadata_columns[(metadata_columns['table_name'] == tbl_name) & 
                            (metadata_columns['key_type'].isin(['FK', 'PF']))]['column_name'].tolist()

def tbl_nkey(tbl_name: str, metadata_columns: pd.DataFrame) -> List[str]:
    check_ambig_table_name(tbl_name, metadata_columns)
    return metadata_columns[(metadata_columns['table_name'] == tbl_name) & 
                            (metadata_columns['natural_key'])]['column_name'].tolist()

def tbl_keys(tbl_name: str, metadata_columns: pd.DataFrame) -> List[str]:
    return list(set(tbl_pkey(tbl_name, metadata_columns) + 
                    tbl_nkey(tbl_name, metadata_columns) + 
                    tbl_fkey(tbl_name, metadata_columns)))

def tbl_link(tbl_name: str, metadata_columns: pd.DataFrame, return_root: bool = True) -> Dict[str, Any]:
    link = {}
    fkey_list = tbl_fkey(tbl_name, metadata_columns)

    if return_root:
        tbl_root = metadata_columns[(metadata_columns['table_name'] == tbl_name) & 
                                    (metadata_columns['key_type'] == 'PK')][['table_schema', 'column_name']]
        link['root'] = {
            'schema': tbl_root['table_schema'].iloc[0],
            'table': tbl_name,
            'pkey': tbl_root['column_name'].tolist(),
            'nkey': tbl_nkey(tbl_name, metadata_columns),
            'fkey': fkey_list
        }

    parents = {}
    for ff in fkey_list:
        pkey = ff
        tbl_parent = metadata_columns[(metadata_columns['column_name'] == pkey) & 
                                      (metadata_columns['key_type'] == 'PK')][['table_schema', 'table_name']]
        nkey = tbl_nkey(tbl_parent['table_name'].iloc[0], metadata_columns)
        fkey = tbl_fkey(tbl_parent['table_name'].iloc[0], metadata_columns)
        parents[tbl_parent['table_name'].iloc[0]] = {
            'schema': tbl_parent['table_schema'].iloc[0],
            'table': tbl_parent['table_name'].iloc[0],
            'pkey': pkey,
            'nkey': nkey,
            'fkey': fkey
        }
    
    link['parents'] = parents
    return link

def tbl_chain(tbl_name: str, metadata_columns: pd.DataFrame, until: List[str] = None) -> Dict[str, Any]:
    chain = {}
    tbl_list = [tbl_name]
    tbl_remaining = True

    tbl_root = metadata_columns[(metadata_columns['table_name'] == tbl_name) & 
                                (metadata_columns['key_type'] == 'PK')][['table_schema', 'column_name']]
    
    chain['root'] = {
        'schema': tbl_root['table_schema'].iloc[0],
        'table': tbl_name,
        'pkey': tbl_root['column_name'].tolist(),
        'nkey': tbl_nkey(tbl_name, metadata_columns),
        'fkey': tbl_fkey(tbl_name, metadata_columns)
    }

    until = until or []

    while tbl_remaining:
        tbl_active = tbl_list.pop(0)
        link_active = tbl_link(tbl_active, metadata_columns, return_root=False)

        if link_active['parents']:
            for ll in link_active['parents'].values():
                if ll['table'] not in until:
                    tbl_list.append(ll['table'])
                chain.setdefault('parents', {})[ll['table']] = ll

        tbl_remaining = bool(tbl_list)

    return chain

def tbl_join(dbcon: ibis.backends.postgres.Backend, link: Dict[str, Any], tbl: ibis.expr.types.relations.Table = None, 
             join: str = "left", by: str = "pkey", columns: List[str] = None) -> ibis.expr.types.relations.Table:
    select_columns = columns != "all"

    if tbl is None:
        print(f"Pulling {link['root']['table']} ... ", end="")
        tbl = dbcon.table(database="public", name=link['root']['table'])

        if select_columns:
            columns_to_select = list(set(link['root']['pkey'] + link['root']['nkey'] + link['root']['fkey'] + (columns or [])))
            tbl = tbl.select(columns_to_select)

        print("done.")

    for pp in link['parents'].values():
        tbl_next = dbcon.table(database="public", name=pp['table'])

        if select_columns:
            columns_to_select = list(set([pp['pkey']] + pp['nkey'] + pp['fkey'] + (columns or [])))
            tbl_next = tbl_next.select(columns_to_select)

        print(f"Joining with {pp['table']} ... ", end="")

        if join == "left":
            tbl = tbl.left_join(tbl_next, tbl[pp[by]] == tbl_next[pp[by]])
        elif join == "full":
            tbl = tbl.outer_join(tbl_next, tbl[pp[by]] == tbl_next[pp[by]])
        elif join == "inner":
            tbl = tbl.inner_join(tbl_next, tbl[pp[by]] == tbl_next[pp[by]])
        elif join == "right":
            tbl = tbl.right_join(tbl_next, tbl[pp[by]] == tbl_next[pp[by]])
        else:
            raise ValueError(f"{join} is not a valid join type... YET. Should it be included?")

        print("done.")

    return tbl
