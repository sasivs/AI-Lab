#include<bits/stdc++.h>
using namespace std;

int editDistance(string s, string t, int n1, int n2){
    // 2-D array to memorize the cost of each sub-problem 
    int sol[n1+1][n2+1];
    for (int i=0; i<=n1; i++){
        for(int j=0; j<=n2; j++){
            //Base cases (when either of the strings is an empty string)
            if (i==0)
                sol[i][j]=j;
            else if (j==0)
                sol[i][j]=i;
            //When the compared characters match, do nothing.
            //Cost of this sub-problem will be same as the cost till its previous
            //characters which is present digonally opposite to current cell in memorized table.
            else if (s[i-1]==t[j-1])
                sol[i][j]=sol[i-1][j-1];
            //Perform all three operations and find the minimum cost among them.
            else
                sol[i][j]=1+min(sol[i-1][j], min(sol[i-1][j-1], sol[i][j-1]));
        }
    }
    return sol[n1][n2];
}

int main(){
    string s,t;
    int test_cases;
    ifstream fin("input.in");
    ofstream fout("output_dp_1.out");

    if(!fin.is_open()) cout<<"Input stream is not ready"<<endl;
    if(!fout.is_open()) cout<<"Output stream is not ready"<<endl;

    fin>>test_cases;
    
    getline(fin,s);
    while(test_cases--){

        getline(fin,s);
        getline(fin,t);

        fout<<"Length of first string: "<<s.length()<<endl<<"Length of second string: "<<t.length()<<endl;

        auto start = chrono::high_resolution_clock::now();
        ios_base::sync_with_stdio(false);

        int result = editDistance(s,t,s.length(),t.length());

        auto end = chrono::high_resolution_clock::now();

        fout<<"No: of operations: "<<result<<endl;

        double time_taken = chrono::duration_cast<chrono::nanoseconds>(end-start).count();
        time_taken = time_taken*1e-9;
        
        fout<<"Time Taken is: "<<fixed<<time_taken<<setprecision(9)<<endl<<endl;
    
    }

    return 0;
}