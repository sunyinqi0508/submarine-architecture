#include "Context.hpp"
using std::vector;
void generating_probes(Context& cxt) {
	auto& probes = cxt.probes;
	// Probes from last rounds are cleared manually,
	probes.clear();
	// TODO: write your algorithm to generate probes.
	for (int i = 0; i < 3; ++i) {
		probes.push_back(cxt.rand99());
	}
	cxt.trench_update1();
}
void set_alert(Context& cxt) {
	auto& probe_results = cxt.probe_results;
	cxt.red_alert = cxt.rand99()%2;
	cxt.trench_update2();
}
int main(int argc, char* argv[])
{
	int port = 5001;

	auto cxt = Context(Context::TRENCH, argc, argv, port);
	while (!cxt.terminated) {
		generating_probes(cxt);
		set_alert(cxt);
	}
	return 0;
}