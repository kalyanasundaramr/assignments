import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_core.prompts import PromptTemplate
import networkx as nx

# Load environment variables from .env file
load_dotenv()

# Flexible Cypher template for Neo4j
CYPHER_GENERATION_TEMPLATE = """You are an expert Neo4j Cypher translator. Convert the user question into a Cypher query.
Always use case-insensitive searches or partial matches using `CONTAINS` when looking up names or properties (e.g., WHERE c.name CONTAINS 'Neo4J' or c.id CONTAINS 'Neo4j').
Do not assume exact ID matching unless explicitly provided. Return only the Cypher query.

Schema:
{schema}

Question: {question}
Cypher Query:"""

CYPHER_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], 
    template=CYPHER_GENERATION_TEMPLATE
)

def build_local_networkx_graph():
    """Builds a local fallback NetworkX graph using your known project triples."""
    G = nx.DiGraph()
    G.add_edge("Emil Eifrem", "Neo4J, Inc.", relation="CO_FOUNDED")
    G.add_edge("Neo4J", "Graphs", relation="STORES_DATA_AS")
    return G

def query_networkx(G, user_query):
    """Smart local fallback that prioritizes intent/relationship matches over raw node name hits."""
    query_lower = user_query.lower()
    results = []
    
    # 1. Check for founder / co-founder intent first (handles typos too)
    founder_keywords = ["founder", "cofounder", "co-founder", "founcder", "co-founcder"]
    if any(kw in query_lower for kw in founder_keywords):
        for u, v, data in G.edges(data=True):
            if data.get("relation") == "CO_FOUNDED":
                results.append(f"👉 {u} co-founded {v}.")
                
    # 2. If no founder intent matched, check for general entity name matches
    if not results:
        for node in G.nodes():
            if node.lower() in query_lower:
                for _, target, data in G.out_edges(node, data=True):
                    rel = data.get("relation", "RELATED_TO")
                    results.append(f"👉 {node} {rel.lower().replace('_', ' ')} {target}.")
                for source, _, data in G.in_edges(node, data=True):
                    rel = data.get("relation", "RELATED_TO")
                    results.append(f"👉 {source} {rel.lower().replace('_', ' ')} {node}.")
                    
    return list(set(results))

def initialize_kgrag():
    required_vars = ["OPENAI_API_KEY", "NEO4J_URI", "NEO4J_USERNAME", "NEO4J_PASSWORD"]
    for var in required_vars:
        if not os.getenv(var):
            raise ValueError(f"Missing required environment variable: {var}")

    print("🔌 Connecting to Neo4j AuraDB...")
    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD")
    )

    print("🔄 Refreshing graph schema...")
    graph.refresh_schema()
    print("✅ Schema refreshed successfully!")

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

    chain = GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        cypher_prompt=CYPHER_PROMPT,
        verbose=False,
        allow_dangerous_requests=True
    )
    
    return chain

def main():
    try:
        neo4j_chain = initialize_kgrag()
    except Exception as e:
        print(f"❌ Failed to initialize Neo4j pipeline: {e}")
        neo4j_chain = None

    # Initialize local NetworkX fallback graph
    nx_graph = build_local_networkx_graph()

    print("\n" + "=" * 60)
    print("🚀 Dual-Engine Knowledge Graph RAG (Neo4j + NetworkX) Ready!")
    print("Type your questions below. Type 'exit' or 'quit' to stop.")
    print("=" * 60)

    while True:
        try:
            user_query = input("\nAsk a question: ").strip()
            
            if user_query.lower() in ["exit", "quit"]:
                print("Exiting KGRAG pipeline. Goodbye!")
                break
                
            if not user_query:
                continue

            print(f"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(f"Query: '{user_query}'")
            print(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            answer_found = False

            # 1. Try Neo4j First
            if neo4j_chain:
                try:
                    print("[Neo4j AuraDB Result]:")
                    response = neo4j_chain.invoke({"query": user_query})
                    result_text = response.get('result', '')
                    if result_text and "I don't know" not in result_text:
                        print(f"👉 Answer: {result_text}")
                        answer_found = True
                    else:
                        print("👉 Neo4j returned no matching context.")
                except Exception as neo4j_err:
                    print(f"⚠️ Neo4j Query Error: {neo4j_err}")

            # 2. Fall back to NetworkX if Neo4j came up empty
            if not answer_found:
                print("\n[NetworkX Local Graph Fallback Result]:")
                nx_results = query_networkx(nx_graph, user_query)
                if nx_results:
                    for res in nx_results:
                        print(res)
                    answer_found = True
                else:
                    print("👉 Local graph fallback found no direct matching facts.")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"❌ Error processing query: {e}")

if __name__ == "__main__":
    main()