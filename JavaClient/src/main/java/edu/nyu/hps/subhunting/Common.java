package edu.nyu.hps.subhunting;
import org.json.*;
import java.util.Arrays;
import java.io.*;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.lang.Thread;
public class Common {
    public static class Instance{
        Socket socket;
        OutputStream os;
        InputStream is;
        byte[] buffer;
        public Instance(int port){
            buffer = new byte[4096];
            while(true){
                try{
                    socket = new Socket("127.0.0.1", port);
                    os = socket.getOutputStream();
                    is = socket.getInputStream();
                    break;
                }
                catch (IOException e){
                    try{
                        Thread.sleep(1);
                    } catch(InterruptedException _){
                        Thread.currentThread().interrupt();
                    }
                }
            }
        }
        public JSONObject recv() throws IOException{
            Arrays.fill(buffer, (byte)0);
            is.read(buffer);
            return new JSONObject(new String(buffer, StandardCharsets.UTF_8));
        }
        public JSONObject send_n_recv(JSONObject data) throws IOException{
            os.write(data.toString().getBytes());
            return recv();
        }
    }
    public static void main( String[] args ) throws IOException
    {
        int port = 5001;
        boolean submarine = false;
        if(args.length < 1 || args[0].equals("Submarine")){
            submarine = true;
            port=5005;
        }
        if(args.length > 1){
            try {port = Integer.parseInt(args[1]);} 
            catch(NumberFormatException _){}
        }
        
        Instance ins = new Instance(port);   
        if(submarine)
            (new SubmarineClient(ins)).run(); 
        else
            (new TrenchManagerClient(ins)).run();
    }
}
