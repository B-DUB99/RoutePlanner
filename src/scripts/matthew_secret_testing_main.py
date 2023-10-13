from data_retriever import data_retriever

d_ret = data_retriever()

d_ret.connect()

amens = d_ret.get_closest_nodes([42, -85])

for a in amens:
    print(f"{a}")

d_ret.close()
