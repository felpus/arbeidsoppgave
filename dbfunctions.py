import pymysql
from decouple import config

from apiconn import getapidata


def getdatabasedata():
    try:
        conn = pymysql.connect(host=config('MYSQL_DATABASE_HOST'),
                               user=config('MYSQL_DATABASE_USER'),
                               passwd=config('MYSQL_DATABASE_PASSWORD'),
                               db=config('MYSQL_DATABASE_DB'))
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM organisasjoner;"
        cursor.execute(query)
        rows = cursor.fetchall()
        # print(rows)
        if len(rows) != 0:
            # for i in rows:
            # print(i)
            # return(i)
            # print(rows)
            return rows
        else:
            print("getdatabasedata(): No organisations exists in the database.")
    except Exception as E:
        print("getdatabasedata() error: ", E)
    finally:
        conn.close()


def filldatabase():
    try:
        data = getapidata()
        conn = pymysql.connect(host=config('MYSQL_DATABASE_HOST'),
                               user=config('MYSQL_DATABASE_USER'),
                               passwd=config('MYSQL_DATABASE_PASSWORD'),
                               db=config('MYSQL_DATABASE_DB'))
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        for i in data["_embedded"]["enheter"]:
            try:
                query = "select organisasjonsnummer from organisasjoner where organisasjonsnummer = %s;"
                cursor.execute(query, i["organisasjonsnummer"])
                row = cursor.fetchone()
                if row is None:
                    query = "INSERT into organisasjoner (organisasjonsnummer, organisasjonsnavn, organisasjonsform) Values (%s, %s, %s);"
                    cursor.execute(query, (
                        i["organisasjonsnummer"], i["navn"], i["organisasjonsform"]["beskrivelse"]))
                    conn.commit()
            except Exception:
                pass
        conn.commit()
    except Exception as E:
        print("filldatabase() error: ", E)
    finally:
        conn.close()


def updategrade(orgnr, grade):
    try:
        conn = pymysql.connect(host=config('MYSQL_DATABASE_HOST'),
                               user=config('MYSQL_DATABASE_USER'),
                               passwd=config('MYSQL_DATABASE_PASSWORD'),
                               db=config('MYSQL_DATABASE_DB'))
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "UPDATE organisasjoner SET karakter = %s WHERE organisasjonsnummer = %s;"
        cursor.execute(query, (grade, orgnr))
        conn.commit()

    except Exception as E:
        print("updategrade() error: ", E)
    finally:
        conn.close()


def verifygrade(orgnr, grade):
    try:
        conn = pymysql.connect(host=config('MYSQL_DATABASE_HOST'),
                               user=config('MYSQL_DATABASE_USER'),
                               passwd=config('MYSQL_DATABASE_PASSWORD'),
                               db=config('MYSQL_DATABASE_DB'))
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT karakter FROM organisasjoner WHERE organisasjonsnummer = %s;"
        cursor.execute(query, orgnr)
        row = cursor.fetchone()
        if row["karakter"] is grade:
            return True
        else:
            return False
    except Exception as E:
        print("get() feilmelding: ", E)
    finally:
        conn.close()


def reset():
    try:
        conn = pymysql.connect(host=config('MYSQL_DATABASE_HOST'),
                               user=config('MYSQL_DATABASE_USER'),
                               passwd=config('MYSQL_DATABASE_PASSWORD'),
                               db=config('MYSQL_DATABASE_DB'))
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "TRUNCATE arbeidsoppgave.organisasjoner;"
        cursor.execute(query)
    except Exception as E:
        print("reset() error: ", E)
    finally:
        conn.close()


def search(searchcriteria, value):
    try:
        conn = pymysql.connect(host=config('MYSQL_DATABASE_HOST'),
                               user=config('MYSQL_DATABASE_USER'),
                               passwd=config('MYSQL_DATABASE_PASSWORD'),
                               db=config('MYSQL_DATABASE_DB'))
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM organisasjoner WHERE ""`" + searchcriteria + "`"" = %s;"
        # print(query)
        cursor.execute(query, value)
        rows = cursor.fetchall()
        # for i in rows:
        # print(i)
        return rows
    except Exception as E:
        print("search() error: ", E)
    finally:
        conn.close()


def getcolumnnames():
    try:
        conn = pymysql.connect(host=config('MYSQL_DATABASE_HOST'),
                               user=config('MYSQL_DATABASE_USER'),
                               passwd=config('MYSQL_DATABASE_PASSWORD'),
                               db=config('MYSQL_DATABASE_DB'))
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = 'organisasjoner';"
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = []
        for i in rows:
            columns.append(i["COLUMN_NAME"])
        return columns
    except Exception as E:
        print("getcolumnnames() error: ", E)
    finally:
        conn.close()
