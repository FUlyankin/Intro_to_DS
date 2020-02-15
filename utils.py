def create_unsolved(dirs, file_solution_marking='solution', solution_start='SOLUTION'):
    """
    Функция идет по папкам из списка `dirs` и чистит все файлы решений
    (т.е. содержащие подстроку `file_solution_marking` в названии).
    Чистка убирает весь код решения на '# TODO:'
    (считается что решение начинается со строки с комментарием содержащей `solution_start`).
    
    Пример ячейки с решением до чистки:
    
    ```
    # SOLUTION:

    s1 = items[1:4]
    s2 = items[-2:]
    res = sum(s1) / sum(s2)
    res
    ```

    Пример ячейки с решением после чистки:
    ```
    # TODO:
    ```
    
    """
    
    
    
    
    import os
    import sys
    import nbformat

    NB_VERSION = 4


    def create_nb(path_to_dir, fname):
        # READ nb
        with open(os.path.join(path_to_dir, fname)) as f:
            nb_src = nbformat.read(f, as_version=NB_VERSION)

        cells = nb_src['cells']
        for cell in cells:
            if cell['cell_type'] == 'code':
                # remove solution
                if 'SOLUTION' in cell['source']:
                    sol_start_idx = cell['source'].find('SOLUTION')
                    cell_src_new = cell['source'][:sol_start_idx] + 'TODO:\n'
                    cell['source'] = cell_src_new
                else:
                    print('[DEBUG] Code cell without solution:')
                    print(cell['source'], end='\n\n')
                # clear outputs
                cell['outputs'] = []
                cell['execution_count'] = 0

        # SAVE new nb
        with open(os.path.join(path_to_dir, fname.replace('_solution', '')), 'w') as f:
            nbformat.write(nb_src, f, version=NB_VERSION)

            
    for path_to_dir in dirs:
        fnames = [fname for fname in os.listdir(
            path_to_dir) if file_solution_marking in fname]
        print(f"[DEBUG]: Creating unsolved for {fnames}")
        for fname in fnames:
            print(f'[DEBUG] Working with {fname}')
            create_nb(path_to_dir, fname)