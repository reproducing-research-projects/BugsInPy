#! /usr/bin/env nix-shell
#! nix-shell -i python3 -p python3Packages.pandas

import pathlib
import pandas

def read_csvs() -> pandas.DataFrame:
    dfs = []
    for condition in ["new-conda", "old-virtualenv"]:
        for version in ["fixed", "buggy"]:
            df = pandas.read_csv(f"../{condition}-{version.split('-')[0]}.csv")
            df["condition"] = [condition] * len(df)
            dfs.append(df)
    df = pandas.concat(dfs)
    for column in ["repo", "version", "result", "condition"]:
        df[column] = df[column].astype("category")
    return df

def classify(df: pandas.DataFrame) -> pandas.DataFrame:
    def _helper(subdf: pandas.DataFrame) -> str:
        if len(subdf) != 2:
            return f"err-{len(subdf)}"
        buggy_result = subdf[subdf["version"] == "buggy"].iloc[0]["result"]
        fixed_result = subdf[subdf["version"] == "fixed"].iloc[0]["result"]
        if buggy_result == "error" or fixed_result == "error":
            return "error"
        elif buggy_result == "fail" and fixed_result == "fail":
            return "both-fail"
        elif buggy_result == "pass" and fixed_result == "pass":
            return "both-pass"
        elif buggy_result == "fail" and fixed_result == "pass":
            return "expected"
        else:
            return buggy_result + "_" + fixed_result
    return (
        df
        .groupby(["condition", "repo", "bugid"])
        .apply(_helper)
        .astype("category")
        .reset_index(name="class_")
    )

def basic_table(subdf: pandas.DataFrame) -> pandas.DataFrame:
    repos = sorted(subdf["repo"].unique())
    table_columns = ["error", "both-fail", "both-pass", "expected"]
    table0 = []
    def gen_row0(name: str, subsubdf: pandas.DataFrame) -> list[str]:
        return " & ".join(
            [name] + [
                f"{subsubdf[table_column]} ({100 * subsubdf[table_column] / subsubdf.sum():.0f}\%)"
                for table_column in table_columns
            ] + [f"{subsubdf.sum()} (100\%)"]) + "\\\\"
    for repo in repos:
        subsubdf = (
            subdf
            [subdf["repo"] == repo]
            ["class_"]
            .value_counts()
        )
        table0.append(gen_row0(repo, subsubdf))
    table0.append("\\midrule")
    subsubdf = subdf["class_"].value_counts()
    table0.append(gen_row0("Total", subsubdf))
    return "\n".join(table0)

df = read_csvs()
df_classified = classify(df)
pathlib.Path("unmodified-reproduction.tex").write_text(basic_table(df_classified[df_classified["condition"] == "old-virtualenv"]))
pathlib.Path("rescued-reproduction.tex").write_text(basic_table(df_classified[df_classified["condition"] == "new-conda"]))
