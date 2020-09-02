from dbfunctions import getdatabasedata


def tables(rows, num_rows, num_cols):
    data = [[j for j in range(num_cols)] for i in range(num_rows)]
    # data[0] = "Org.nummer", "Organisasjonsnavn", "Organisasjonsform", "Karakter"
    for item in range(0, len(rows)):
        # print(rows[item])
        data[item] = [rows[item]["organisasjonsnummer"], rows[item]["organisasjonsnavn"],
                      rows[item]["organisasjonsform"],
                      rows[item]["karakter"]]
    return data


def formatdatatable():
    rows = getdatabasedata()
    data = tables(rows, num_rows=len(rows), num_cols=4)
    return data