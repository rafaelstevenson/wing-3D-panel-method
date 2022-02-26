#include <iostream>
#include <fstream>
#include <vector>
#include <random>
#include <stdlib.h>
#include <math.h>

using namespace std;

/*definition of a node*/
struct Node
{
	double pos[3];	
	Node(double x, double y, double z) {pos[0]=x;pos[1]=y;pos[2]=z;}	
};

/*definition of a quad*/
struct Quad
{
	int con[4];
	double area;
	double Cp;
	Quad(int n1, int n2, int n3, int n4) {con[0]=n1;con[1]=n2;con[2]=n3;con[3]=n4;}
};

/*definition of a surface*/
struct Panel
{
	vector <Node> nodes;
	vector <Quad> elements;
};

void Output(Panel &panel);

int main()
{
    /*open file*/
	ifstream in("Panel.dat");
	if (!in.is_open()) {cerr<<"Failed to open input file";return -1;}
	
	/*read number of nodes and elements*/
	int n_nodes, n_elements;
	in>>n_nodes>>n_elements;
	cout<<"Mesh contains "<<n_nodes<<" nodes and "<<n_elements<<" elements"<<endl;

	/*instantiate panel*/
	Panel panel;
	
	/*read the nodes*/
	for (int n=0;n<n_nodes;n++)
	{
		int index;
		double x, y, z;

		in >> index >> x >> y >> z;
		if (index!=n+1) cout<<"Inconsistent node numbering"<<endl;
			
		panel.nodes.emplace_back(x,y,z);		
	}
	
	//read elements, this will also contain edges
	for (int e=0;e<n_elements;e++)
	{
		int index, type;
		int n1, n2, n3, n4;

		in >> index >> type;
		
		if (type!=9) {string s; getline(in,s);continue;}
		
		in >> n1 >> n2 >> n3 >> n4;
		
		panel.elements.emplace_back(n1-1, n2-1, n3-1, n4-1);	//if nodes indexing starts from 1	
	}

	//read element data
	for (int e=0;e<n_elements;e++)
	{
		int index;
		double Cp,Area;

		in >> index;
	
		in >> Cp >> Area;
		
		panel.elements[e].Cp = Cp;
		panel.elements[e].area = Area;
	}

    Output(panel);
}


void Output(Panel &panel)
{
    ofstream out("Panel.vtu");
	if (!out.is_open()) {cerr<<"Failed to open output file "<<endl;exit(-1);}
	
	/*header*/
	out<<"<?xml version=\"1.0\"?>\n";
	out<<"<VTKFile type=\"UnstructuredGrid\" version=\"0.1\" byte_order=\"LittleEndian\">\n";
	out<<"<UnstructuredGrid>\n";
	out<<"<Piece NumberOfPoints=\""<<panel.nodes.size()<<"\" NumberOfVerts=\"0\" NumberOfLines=\"0\" ";
	out<<"NumberOfStrips=\"0\" NumberOfCells=\""<<panel.elements.size()<<"\">\n";
	
	/*points*/
	out<<"<Points>\n";
	out<<"<DataArray type=\"Float32\" NumberOfComponents=\"3\" format=\"ascii\">\n";
	for (Node &node: panel.nodes)
		out<<node.pos[0]<<" "<<node.pos[1]<<" "<<node.pos[2]<<"\n";		
	out<<"</DataArray>\n";
	out<<"</Points>\n";

	/*Cells*/
	out<<"<Cells>\n";
	out<<"<DataArray type=\"Int32\" Name=\"connectivity\" format=\"ascii\">\n";
	for (Quad &quad: panel.elements)
		out<<quad.con[0]<<" "<<quad.con[1]<<" "<<quad.con[2]<<" "<<quad.con[3]<<"\n";
	out<<"</DataArray>\n";
	
	out<<"<DataArray type=\"Int32\" Name=\"offsets\" format=\"ascii\">\n";
	for (int e=0; e<panel.elements.size();e++)
		out<<(e+1)*4<<" ";
	out<<"\n";
	out<<"</DataArray>\n";
	
	out<<"<DataArray type=\"UInt8\" Name=\"types\" format=\"ascii\">\n";
	for (int e=0; e<panel.elements.size();e++)
		out<<"9 ";
	out<<"\n";
	out<<"</DataArray>\n";		
	out<<"</Cells>\n";

	/*save Cp data*/
	out<<"<CellData Scalars=\"properties\">\n";
	out<<"<DataArray type=\"Float32\" Name=\"cp\" format=\"ascii\">\n";
	for (Quad &quad:panel.elements)
		out<<quad.Cp<<" ";
		//out<<1<<" ";
	out<<"\n";
	out<<"</DataArray>\n";

	/*save area data*/
	out<<"<DataArray type=\"Float32\" Name=\"panel_area\" format=\"ascii\">\n";
	for (Quad &quad:panel.elements)
		out<<quad.area<<" ";
		//out<<1<<" ";
	out<<"\n";
	out<<"</DataArray>\n";
	
	out<<"</CellData>\n";
	
	out<<"</Piece>\n";
	out<<"</UnstructuredGrid>\n";
	out<<"</VTKFile>\n";

	out.close();
}