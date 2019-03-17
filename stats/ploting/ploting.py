import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import six


def prepare_dataframe(data) -> pd.DataFrame:
    df = pd.DataFrame.from_dict(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df.set_index('timestamp', inplace=True)
    df.sort_index(inplace=True)
    return df


def post_generate(plt):
    plt.spines['right'].set_visible(False)
    plt.spines['top'].set_visible(False)
    plt.spines['left'].set_visible(False)
    plt.spines['bottom'].set_visible(False)

    for tick in filter(lambda x: x >= 0, plt.get_yticks()):
        plt.axvline(x=tick, linestyle='dashed', alpha=0.4, color='#eeeeee',
                    zorder=1)

    return plt


def get_month_amount_stat(data):
    df = prepare_dataframe(data)

    g = df.groupby(pd.Grouper(freq="M"))

    frame = g['amount'].sum().to_frame()

    frame['timestamp'] = frame.index
    frame['month'] = frame['timestamp'].dt.strftime('%d/%m/%Y')
    frame.reset_index(drop=True, inplace=True)
    frame.drop(['timestamp'], axis=1)
    frame['amount'] = frame['amount'].round(2)

    frame = frame[['month', 'amount']]

    size = (np.array(frame.shape[::-1]) + np.array([0, 1])) * np.array(
        [2.650, 0.625])

    _, ax = plt.subplots(figsize=size)
    ax.axis('off')

    mpl_table = ax.table(
        cellText=frame.values,
        bbox=[0, 0, 1, 1],
        colLabels=frame.columns,
        cellLoc='center',
    )

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(14)

    row_colors = ['#f1f1f2', 'w']

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor('w')
        if k[0] == 0 or k[1] < 0:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor('#86bf91')
        else:
            cell.set_facecolor(row_colors[k[0] % len(row_colors)])
    return ax


def get_month_stat(data):
    df = prepare_dataframe(data)

    g = df.groupby(pd.Grouper(freq="M"))

    total = round(df['amount'].sum(), 2)

    plt = g.sum().plot(figsize=(15, 8), color='#86bf91', fontsize=12,
                       title=f'Total: {total}', grid=True, legend=False,
                       kind='line')

    plt.set_ylabel("Amount", labelpad=20, weight='bold', size=12)
    plt.set_xlabel("Month", labelpad=20, weight='bold', size=12)

    plt.tick_params(axis="both", which="both", bottom=False, top=False,
                    labelbottom=True, left=False, right=False, labelleft=True)

    return post_generate(plt)


def get_category_stat(data):
    df = prepare_dataframe(data)

    g = df.groupby(by='category')
    sm = g.sum().sort_values(by='amount', ascending=True)

    total = round(sm['amount'].sum(), 2)

    plt = sm.plot(figsize=(8, 10), color='#86bf91', fontsize=12, zorder=2,
                  width=0.85, title=f'Total: {total}', kind='barh',
                  legend=False, )

    plt.set_ylabel("Category", labelpad=20, weight='bold', size=12)
    plt.set_xlabel("Amount", labelpad=20, weight='bold', size=12)

    for y, x in enumerate(sm['amount']):
        percentage = round(x * 100 / total, 2)
        plt.annotate(
            f'{round(x, 2)} / {percentage}%', xy=(x, y), va='center',
        )

    return post_generate(plt)
