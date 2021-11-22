package edu.nyu.hps.subhunting;
import edu.nyu.hps.subhunting.Common.Instance;
import org.json.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.io.IOException;
public class TrenchManagerClient
{
    Instance ins;
    int m, L, d, y, r, p;
    JSONObject output1, output2;

    public TrenchManagerClient(Instance ins) throws IOException {
        this.ins = ins;
        JSONObject data = ins.recv();
        this.m = data.getInt("m");
        this.L = data.getInt("L");
        this.d = data.getInt("d");
        this.y = data.getInt("y");
        this.r = data.getInt("r");
        this.p = data.getInt("p");
        output1 = new JSONObject();
        output2 = new JSONObject();
    }
    public void run() throws IOException{
        Random rand = new Random();
        boolean terminated = false;
        List<Integer> probes = new ArrayList<Integer>();
        List<Boolean> probe_results = new ArrayList<Boolean>();
        while(!terminated){
            // TODO: generate movements.
            probes.clear();
            for(int i = 0; i < 3; ++i)
                probes.add(rand.nextInt(99));
            output1.put("probes", probes);
            JSONObject res = ins.send_n_recv(output1);
            List<Object> arr = res.getJSONArray("probe_results").toList();
            probe_results.clear();
            for (Object r : arr) {
                probe_results.add((Boolean)r);
            }
            System.out.println(probe_results);
            output2.put("red_alert", rand.nextInt(1) < 1);
            res = ins.send_n_recv(output2);
            terminated = res.getBoolean("terminated");
        }
    }
}
