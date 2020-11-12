from EleNa.src.app.data_model import data_model
import os


def main():
    os.chdir('../')
    d = data_model.DataModel('Hadley, MA')

    # Check Config values
    print(d.config)

    # Check Graph
    print(d.G.number_of_nodes())

    # Load new graph by address
    d1 = data_model.DataModel('Northampton, MA')
    print(d1.G.number_of_nodes())

    exit(0)


if __name__ == "__main__":
    main()
