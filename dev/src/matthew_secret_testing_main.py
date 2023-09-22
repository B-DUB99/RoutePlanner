from data_retriever import data_retriever

d_ret = data_retriever()

d_ret.connect()

amens = d_ret.get_amenities('Worlds of Wonder')

for a in amens:
    print(f"{a[0]['lat']}")

d_ret.close()
