import pandas as pd
import matplotlib.pyplot as plt

def main():
    df = pd.read_csv('replies_clean.csv')

    #Crear una grafica
    df.groupby('user').count().plot(kind='barh')
    plt.subplots_adjust(left=0.28, right=0.9, top=0.9, bottom=0.1)
    plt.title('Tweets por usuario')
    plt.xlabel('Tweets')
    plt.ylabel('Usuario')
    plt.xticks(rotation='vertical')
    plt.show()

if __name__ == '__main__':
    main()
