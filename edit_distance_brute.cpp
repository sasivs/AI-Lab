#include<bits/stdc++.h>
#include <chrono>
using namespace std;

int editDistance(string s, string t, int n1, int n2){
    /* Base cases(either of the strings is an empty string) */
    if (n1 == 0) return n2;
    if (n2 == 0) return n1;
    /*
        if the characters are matching at the end, then do nothing and move to next character.
    */
    if (s[n1-1] == t[n2-1]) return editDistance(s,t,n1-1,n2-1);
    /*
        if they do not match, then apply all three operations and choose the minimum of the three using recursive calls.
    */
    else return 1 + min(editDistance(s,t,n1,n2-1), min(editDistance(s,t,n1-1,n2-1),editDistance(s,t,n1-1,n2)));
}

int main(){
    string s,t;
    int test_cases;
    //Take input from a file
    ifstream fin("input.in");
    ofstream fout("output_brute.out");
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

        //Calculate time taken to solve each test case
        double time_taken = chrono::duration_cast<chrono::nanoseconds>(end-start).count();
        time_taken = time_taken*1e-9;
        
        fout<<"Time Taken is: "<<fixed<<time_taken<<setprecision(9)<<endl<<endl;
    
    }

    return 0;
}