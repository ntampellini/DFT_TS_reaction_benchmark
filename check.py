import os
from subprocess import getoutput
from firecode.units import EH_TO_KCAL
from rich.traceback import install
install(show_locals=True)

def get_energy(file):
    return float(getoutput(f'grep energy {file}').split()[5][:-1])

def get_natoms(file):
    return float(getoutput(f'head {file} -n 1').split()[0])

def main():
    HERE = '/home/Coding/rowan_benchmark/data'
    os.chdir(HERE)

    folders = [name for name in os.listdir() if os.path.isdir(name)]
    for f, folder in enumerate(folders, start=1):
        print(f'{f}. {folder}')
        reactants_energy, products_energy, ts_energy = 0., 0., 0.
        reactants_natoms, products_natoms, ts_natoms = 0, 0, 0
        os.chdir(HERE)
        os.chdir(folder)

        files = os.listdir()
        for file in files:
            assert file.endswith('.xyz')
            energy = get_energy(file)
            natoms = get_natoms(file)

            if file.startswith('reactant_'):
                reactants_energy += energy
                reactants_natoms += natoms

            elif file.startswith('product_'):
                products_energy += energy
                products_natoms += natoms

            elif file.startswith('TS'):
                ts_energy += energy
                ts_natoms += natoms

            else:
                raise Exception(file)
            
        if reactants_energy == 0:
            print(f'    -> {folder} - missing reagents\n')
            continue

        if products_energy == 0:
            print(f'    -> {folder} - missing products\n')
            continue

        if ts_energy == 0:
            print(f'    -> {folder} - missing TS\n')
            continue

        # rxn_fwd_energy = (ts_energy - reagents_energy) * EH_TO_KCAL
        # if not 5 < rxn_fwd_energy < 50:
        #     print(f'{folder} - fwd_e = {rxn_fwd_energy:.2f} kcal/mol')

        # rxn_bwd_energy = (ts_energy - products_energy) * EH_TO_KCAL
        # if not 5 < rxn_bwd_energy < 50:
        #     print(f'{folder} - bwd_e = {rxn_bwd_energy:.2f} kcal/mol')       

        assert ts_natoms == products_natoms, (folder, file, ts_natoms, products_natoms)
        assert ts_natoms == reactants_natoms, (folder, file, ts_natoms, reactants_natoms)

        print()


if __name__ == '__main__':
    main()