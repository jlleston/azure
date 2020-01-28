from gremlin_python.driver import client, serializer
import sys, traceback

CLEANUP_GRAPH = "g.V().drop()"

INSERT_NATIONAL_PARK_VERTICES = [
   "g.addV('Park').property('id', 'p1').property('name', 'Yosemite').property('Feature', 'El Capitan').property('pk','pk')",
   "g.addV('Park').property('id', 'p2').property('name', 'Joshua Tree').property('Feature', 'Yucca Brevifolia').property('pk','pk')",
   "g.addV('State').property('id', 's1').property('name', 'California').property('Location', 'USA').property('pk','pk')",
   "g.addV('Ecosystem').property('id', 'e1').property('name', 'Alpine').property('pk','pk')",
   "g.addV('Ecosystem').property('id', 'e2').property('name', 'Desert').property('pk','pk')",
   "g.addV('Ecosystem').property('id', 'e3').property('name', 'High Altitude').property('pk','pk')"
]

INSERT_NATIONAL_PARK_EDGES = [
   "g.V('p1').addE('is in').to(g.V('s1'))",
   "g.V('p2').addE('is in').to(g.V('s1'))",
   "g.V('p1').addE('has ecosystem of').to(g.V('e1'))",
   "g.V('p2').addE('has ecosystem of').to(g.V('e2'))",
   "g.V('p1').addE('has ecosystem of').to(g.V('e3'))",
   "g.V('p2').addE('has ecosystem of').to(g.V('e3'))"
]

COUNT_VERTICES = "g.V().count()"

def cleanup_graph(client):
   print("\tExecuting Gremlin query:\n\t{0}".format(CLEANUP_GRAPH))
   callback = client.submitAsync(CLEANUP_GRAPH)
   if callback.result() is not None:
       print("\tCleaned up the graph!")
   print("\n")


def create_national_park_vertices(client):
   for query in INSERT_NATIONAL_PARK_VERTICES:
       print("\tExecuting Gremlin query:\n\t{0}\n".format(query))
       callback = client.submitAsync(query)
       if callback.result() is not None:
           print("\tInserted this vertex:\n\t{0}\n".format(callback.result().one()))
       else:
           print("This query failed: {0}".format(query))
   print("\n")


def create_national_park_edges(client):
   for query in INSERT_NATIONAL_PARK_EDGES:
       print("\tExecuting Gremlin query:\n\t{0}\n".format(query))
       callback = client.submitAsync(query)
       if callback.result() is not None:
           print("\tInserted this edge:\n\t{0}\n".format(callback.result().one()))
       else:
           print("This query failed:\n\t{0}".format(query))
   print("\n")


def count_national_park_vertices(client):
   print("\tExecuting Gremlin query:\n\t{0}".format(COUNT_VERTICES))
   callback = client.submitAsync(COUNT_VERTICES)
   if callback.result() is not None:
       print("\tCount of vertices: {0}".format(callback.result().one()))
   else:
       print("This query failed: {0}".format(COUNT_VERTICES))
   print("\n")

try:
   client = client.Client('wss://jllgraphdb.gremlin.cosmos.azure.com:443/', 'g',
                          username="/dbs/parks/colls/national_parks",
                          password="GJbbcBvTkFXvZ5t9AWJtVCcAC5jIg07yyKZGzbrS0LahC0pVwpWtrkAoibstgi0HXB2xYVejwoLfbCBDCkGG4g==",
                          message_serializer=serializer.GraphSONSerializersV2d0()
                          )

   # Drop the entire Graph
   print("Cleaning up the National Parks graph...")
   cleanup_graph(client)

   # Insert all vertices
   print("Inserting National Parks vertices...")
   create_national_park_vertices(client)

   # Create edges between vertices
   print("Inserting National Parks edges...")
   create_national_park_edges(client)

   # Count all vertices
   print("Counting graph vertices...")
   count_national_park_vertices(client)

except Exception as e:
   print('An exception was thrown: {0}'.format(e))
   traceback.print_exc(file=sys.stdout)
   sys.exit(1)

print("\nDONE")
