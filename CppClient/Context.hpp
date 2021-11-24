#ifdef _WIN32
    #define _CRT_SECURE_NO_WARNINGS
    #define _WINSOCK_DEPRECATED_NO_WARNINGS
    #include <WinSock2.h>
    #undef max
    #undef min
#else
    #include <sys/socket.h>
    #include <netinet/in.h>
    #include <arpa/inet.h>
#endif

#include <sys/types.h>
#include <fcntl.h>

#include <cstdio>
#include <cstring>
#include <string>
#include <cstdlib>
#include <chrono>
#include <vector>
#include <thread>
#include <random>

using std::string;
using std::vector;
struct Context
{
private:
    int s;
    int port = 5001;
    const char *addr;
    const bool role;
    void inline static ws(const char *&buf)
    {
        while (*buf == ' ' || *buf == '\t' || *buf == '\n' || *buf == '\r')
            ++buf;
    }
    int static parseInt(const char *&buf)
    {
        ws(buf);
        int res = 0;
        while (*buf >= '0' && *buf <= '9')
            res = res * 10 + *buf++ - '0';
        return res;
    }

// MINIMAL JSON PARSER. 
    class JsonParser{
    public:
        char buffer[4096];
        const char *next(const char *&pos, const char d = '\"')
        {
            while (*pos != d && *pos)
                ++pos;
            pos += *pos != 0;
            return pos;
        }
        const char *getField(const char *buf, const char *field)
        {
            next(buf);
            size_t f_length = strlen(field);
            while (*buf)
            {
                auto start = buf;
                auto end = next(buf) - 1;
                size_t length = end - start;
                bool found = true;
                if (f_length == length)
                {
                    for (int i = 0; start < end; ++start, ++i)
                        if (*start != field[i])
                        {
                            found = false;
                            break;
                        }
                    if (found)
                    {
                        if (*next(buf, ':'))
                        {
                            ws(buf);
                            return buf;
                        }
                    }
                }
                buf = next(buf);
            }
            printf("Error: cannot find field %s\n", field);
            return 0;
        }
        template <typename T = int>
        void getList(const char *field, vector<T> &list)
        {
            const char *buf = getField(buffer, field);
            list.clear();
            if (buf)
            {
                auto start = next(buf, '[');
                auto end = next(buf, ']');
                while (start < end)
                {
                    list.push_back(_getInt_impl(start));
                    start = next(start, ',');
                }
            }
        }    
        int _getInt_impl(const char* buf){
            ws(buf);
            if (*buf == 't' || *buf == 'T')
                return 1;
            else
                return parseInt(buf);
        }
        int getInt(const char *field)
        {
            const char* buf = getField(buffer, field);
            int ret = 0;
            if (buf)
                return _getInt_impl(buf);
            return 0;
        }    
         
        int getBool(const char *field)
        {
            return getInt(field);
        }
    } parser;
    class JsonGenerator
    {
        string json;
        bool start = true;

    public:
        void writeField(const char *field)
        {
            if (!start)
                json += ", ";
            json += '\"';
            json += field;
            json += "\" : ";
        }
        void writeBool(bool b)
        {
            json += b ? "true" : "false";
        }
        void writeInt(int i)
        {
            json += std::to_string(i);
        }
        void writeList(vector<int> &list)
        {
            json += '[';
            bool first = true;
            for (const auto &li : list)
            {
                if (!first)
                    json += ", ";
                else
                    first = false;
                writeInt(li);
            }
            json += ']';
        }
        void newJson()
        {
            json.clear();
            start = true;
            json += '{';
        }
        void finalize(int s)
        {
            json += '}';
            send(s, json.c_str(), json.size(), 0);
        }
    } json;

public:
    enum ROLE{ SUBMARINE, TRENCH };
// __IN__
    int m, l, position;
    int d, y, r, p, L;
// __OUT__
    int movement;
    bool terminated, probed;
    bool red_alert;
    vector<bool> probe_results;
    vector<int> probes;
// CONTEXT INITIALIZATIONS (SOCKET, ETC.)
    Context(ROLE role, int argc = 0, char** argv = 0, int port = 5001, const char *addr = "127.0.0.1")
        : port(port), addr(addr), role(role), terminated(false)
    {
        for (--argc; argv && argc > 0; --argc){
            const char* argi = argv[argc];
            int _port = parseInt(argi);
            if (_port > 0)
            {	
                this->port = _port;
                break;
            }
        }
        start_socket();
        get_initials();
        std::random_device rd;
        engine = std::mt19937{rd()};
    }
    ~Context()
    {
#ifdef _WIN32
        WSACleanup();
#endif
    }    
    
    void start_socket()
    {
        using namespace std::chrono_literals;
#ifdef _WIN32
        WSADATA wsaData;
        WORD wVersionRequested = MAKEWORD(2, 2);
        WSAStartup(wVersionRequested, &wsaData);
#endif
        s = socket(AF_INET, SOCK_STREAM, 0);
        const char one = 1;
        setsockopt(s, SOL_SOCKET, SO_REUSEADDR, &one, sizeof(int));
#ifdef SO_REUSEPORT
        setsockopt(s, SOL_SOCKET, SO_REUSEPORT, &one, sizeof(int));
#endif
        struct sockaddr_in saddr;
        memset(&saddr, 0, sizeof(saddr));
        saddr.sin_family = AF_INET;
        saddr.sin_port = htons(port);
        saddr.sin_addr.s_addr = inet_addr(addr);
        while (connect(s, (struct sockaddr *)&saddr, sizeof(saddr)) < 0)
        {
            printf("Connection fails... retrying\n");
            std::this_thread::sleep_for(10ns);
        }
    }
    void fetch_data()
    {
        recv(s, parser.buffer, sizeof(parser.buffer), 0);
    }
// FETCH INITIAL VALUES
    void get_submarine_initials()
    {
        position = parser.getInt("position");
    }
    void get_trench_initials()
    {
        d = parser.getInt("d");
        y = parser.getInt("y");
        r = parser.getInt("r");
        p = parser.getInt("p");
    }
    void get_initials()
    {
        fetch_data();
        m = parser.getInt("m");
        L = parser.getInt("L");
        if (role == SUBMARINE)
            get_submarine_initials();
        else
            get_trench_initials();
    }
// UPDATE METHODS
    void submarine_update()
    {
        json.newJson();
        json.writeField("movement");
        json.writeInt(movement);
        json.finalize(s);
        fetch_data();
        terminated = parser.getBool("terminated");
        probed = parser.getBool("probed");
    }
    void trench_update1()
    {
        json.newJson();
        json.writeField("probes");
        json.writeList(probes);
        json.finalize(s);
        fetch_data();
        parser.getList("probe_results", probe_results);
    }
    void trench_update2()
    {
        json.newJson();
        json.writeField("red_alert");
        json.writeBool(red_alert);
        json.finalize(s);
        fetch_data();
        terminated = parser.getBool("terminated");
    }

//  REMOVE THEM IF YOU DON'T NEED RANDOM NUMBER GENERATION
    std::mt19937 engine;
    using randint = std::uniform_int_distribution<int>;
    randint _random0_99 = randint(0, 99);
    randint _randmove = randint(0, 3);
    int rand99() { return _random0_99(engine); }
    int randmove() { return _randmove(engine); }
};
