from datetime import timedelta
import pandas as pd


# ユーザ名と日付のカラム
user_col_name = 'user'
date_col_name = 'date'

# 日付のフォーマット
date_format = '%Y-%m-%d'

# 日付の差の閾値
days_threshold = 30


def main(filename: str = 'df_sample.csv'):
    df = pd.read_csv(filename)

    # 日付を文字列からdatetime64[ns]に変換
    df[date_col_name] = pd.to_datetime(df[date_col_name], format=date_format)

    # 必要なカラムだけ選択し、日付の重複を削除
    df = df[[user_col_name, date_col_name]].drop_duplicates()

    # ユーザ名順、新しい順に、並び替え
    df = df.sort_values(
        by=[user_col_name, date_col_name], ascending=[True, False])

    # 2日以上購入しているユーザの、最新とその前のデータ
    dfg = df.groupby(user_col_name)[date_col_name]
    df_latest = pd.DataFrame(dfg.nth(0)).reset_index()
    df_second_latest = pd.DataFrame(dfg.nth(1)).reset_index()
    df2 = df_latest.merge(
        df_second_latest, on=user_col_name, how='inner',
        suffixes=('_latest', '_second_latest')
    )

    # 日付の差分を計算
    df2['date_diff'] = df2[f'{date_col_name}_latest'] - \
        df2[f'{date_col_name}_second_latest']

    # 閾値以上のデータを取得
    dm = df2[df2['date_diff'] >= timedelta(days=days_threshold)]

    print(dm)

    # dmを保存
    dm.to_csv('dm.csv', index=False)

    # ユーザ名だけ保存
    dm[[user_col_name]].to_csv('user.csv', index=False)


if __name__ == '__main__':
    main()
