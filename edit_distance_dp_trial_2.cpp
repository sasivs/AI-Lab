#include<bits/stdc++.h>
using namespace std;

int editDistance(string s, string t, int n1, int n2){
    //At every stage, we require only the memorized values of the previous row in the table
    //So, use only two rows in the table.
    int sol[2][n1+1];
    
    for(int j=0; j<=n2; j++){
        for (int i=0; i<=n1; i++){
            //Base Cases
            if (i==0)
                sol[j%2][i]=j;
            else if (j==0)
                sol[j%2][i]=i;
            //When both characters match
            else if (s[i-1]==t[j-1])
                sol[j%2][i]=sol[(j-1)%2][i-1];
            //if they do not match, try all the three operations and find the minimum.
            else
                sol[j%2][i]=1+min(sol[(j-1)%2][i], min(sol[(j-1)%2][i-1], sol[j%2][i-1]));
        }
    }
    return sol[n2%2][n1];
}

int main(){
    string s,t;
    int test_cases;
    ifstream fin("input.in");
    ofstream fout("output_dp_2.out");

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