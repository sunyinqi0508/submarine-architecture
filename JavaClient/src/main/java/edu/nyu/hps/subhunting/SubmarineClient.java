package edu.nyu.hps.subhunting;
import edu.nyu.hps.subhunting.Common.Instance;
import org.json.*;
import java.util.Random;
import java.io.IOException;
public class SubmarineClient
{
    Instance ins;
    int m, L, position;
    JSONObject output = new JSONObject();

    public SubmarineClient(Instance ins) throws IOException {
        this.ins = ins;
        JSONObject data = ins.recv();
        this.m = data.getInt("m");
        this.L =  data.getInt("L");
        this.position = data.getInt("position");
        System.out.println("Submarine Client started.");
    }
    public void run() throws IOException{
        Random rand = new Random();
        boolean terminated = false, probed = false;

        while(!terminated){
            // TODO: generate movements.
            output.put("movement", rand.nextInt(2) - 1);


            JSONObject res = ins.send_n_recv(output);
            terminated = res.getBoolean("terminated");
            probed = res.getBoolean("probed");
        }
    }
}
