#include "Context.hpp"
int main(int argc, char* argv[]) {
	int port = 5005;

    auto cxt = Context(Context::SUBMARINE, argc, argv, port);
    // *initials* : will not change during execution
    const int& m = cxt.m;
    const int& L = cxt.L;
    // Note: this is the initial position which will not be updated ever.
    const int& initial_position = cxt.position; 

    // *status* : will be updated at each time slot
    const bool& terminated = cxt.terminated;
    const bool& probed = cxt.probed; // returns whether the current position has ever been probed.

    // algorithm outputs
    int& movement = cxt.movement;

    while (!terminated) {
        // TODO: update the `movement` variable with your algorithm
        movement = cxt.randmove();

        cxt.submarine_update();
    }
    return 0;
}