from dependencies import *

userdata = pd.read_csv('data/yelp/user.csv', low_memory=False)
userdata = userdata.fillna('NaN')
userdata['elite'] = [0 if x == 'NaN' else len(x.split(',')) for x in userdata['elite'].values]

# Map each user id to a number
uid2num = {k:v for k,v in zip(userdata['user_id'].values,range(len(userdata['user_id'].values)))}
num2uid = {k:v for v,k in uid2num.items()}

#Create an adjacency matrix for users who have atleat one freind
udata = userdata[userdata['friends'] != 'None']
adj = {uid2num[k]:[uid2num[x] for x in v.split(', ') if x in uid2num] for k,v in zip(udata['user_id'].values,udata['friends'].values)}


g = nx.Graph()
g.add_nodes_from(adj.keys())
for i in adj.keys():
	g.add_edges_from([(i,k) for k in adj[i]])


print(g.number_of_nodes())
print(g.number_of_edges())
#nx.is_connected(g)
print("Number of connected components",nx.number_connected_components(g))
#gc = max(nx.connected_component_subgraphs(g), key=len)

components = sorted(nx.connected_component_subgraphs(g), key=len,reverse = True)
gc = components[1]

pickle.dump(components, open( "graph_components_apr29.p", "wb" ) )
