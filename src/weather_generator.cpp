#include <iostream>
#include <string>
#include <vector>
#include <math.h>

using namespace std;

struct state
{
    double sunny;
    double cloudy;
    double rainy;

    state(double sunny1, double cloudy1, double rainy1)
    {
        if ( sunny1 + cloudy1 + rainy1 != 1.0 )
        {
            cerr<<"Invalid Markov Chain; edges do not add to 1.\n";
            exit(1);
        }
        if ( sunny1 < 0 || sunny1 > 1 || rainy1 < 0 || rainy1 > 1 || 
             cloudy1 < 0 || cloudy1 > 1 )
        {
            cerr<<"Invalid Markov Chain; weights for edges are not between 0 and 1.\n";
            exit(1);
        }
        sunny = sunny1;
        cloudy = cloudy1;
        rainy = rainy1;
    }
};

string state_generator_init()
{
    string random_state;
    double u = (double) (random()) / RAND_MAX;
    if ( u <= .33)
        random_state = "sunny";

    else if ( u > .33 and u <= .67)
        random_state = "cloudy";

    else random_state = "rainy";

    return random_state;
}

string state_generator(string current_state)
{
    string next_state;
    double u = (double) (random()) / RAND_MAX;
    if ( current_state == "sunny")
    {
        if ( u <= .8 )
            next_state = "sunny";

        else next_state = "cloudy";
    }

    else if ( current_state == "cloudy" )
    {
        if ( u <= .4 )
            next_state = "sunny";
        
        else if ( u > .4 and u <= .8)
            next_state = "cloudy";

        else next_state = "rainy";
    }

    else if ( current_state == "rainy" )
    {
        if ( u <= .2 )
            next_state = "sunny";
        
        else if ( u > .2 and u <= .8)
            next_state = "cloudy";

        else next_state = "rainy";
    }

    return next_state;
}

double entropy(double station_sunny, double station_cloudy, double station_rainy)
{
    //equation for entropy given some stationary distribution
    return -1*station_sunny*log(station_sunny)+station_cloudy*log(station_cloudy)
           +station_rainy*log(station_rainy); 
}
int main()
{
    //states
    state sunny(.8, .2, 0);
    state cloudy(.4, .4, .2);
    state rainy(.2,.6,.2);
    double station_sunny = 0;
    double station_cloudy = 0;
    double station_rainy = 0;
    vector<string> state_sequence;
    int i = 1;
    string init_state = state_generator_init();
    state_sequence.push_back(init_state);
    while (i<1000)
    {
        state_sequence.push_back(state_generator(state_sequence[i-1]));
        if (state_sequence[i] == "sunny")
            station_sunny = station_sunny + 1;
        else if (state_sequence[i] == "cloudy")
            station_cloudy = station_cloudy + 1;
        else if (state_sequence[i] == "rainy")
            station_rainy = station_rainy + 1;
        i++;
    }  
    station_sunny = station_sunny/1000;
    station_cloudy = station_cloudy/1000;
    station_rainy = station_rainy/1000;

    cout<<"stationary sunny: "<<station_sunny<<" stationary cloudy: "<<
           station_cloudy<<" stationary rainy: "<<station_rainy<<endl;
    cout<<entropy(station_sunny,station_cloudy,station_rainy)<<endl;

    return 0;
}