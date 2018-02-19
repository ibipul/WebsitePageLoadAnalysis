import dns
import dns.name
import dns.query
import dns.resolver
import time
import sys

class myDig:

    _STATIC_ROOT_SERVER_NAMES = ['a.root-servers.net', 'b.root-servers.net',
              'c.root-servers.net', 'd.root-servers.net', 'e.root-servers.net',
              'f.root-servers.net','g.root-servers.net','h.root-servers.net',
              'i.root-servers.net','j.root-servers.net','k.root-servers.net',
              'l.root-servers.net','m.root-servers.net']

    def __init__(self):
        # Set up the class to Fetch the Root-server IPS
        self.sys_r = self.get_sys_resolver()
        self.root_server_addresses = self.get_root_server_ips(sys_resolver=self.sys_r)

    def get_sys_resolver(self):
        """
        Set up dnspython default, dns-resolver
        Used by the constructor method to fetch the ip-addresses of the .
        root-server list.
        :return:
        dnspython resolver object
        """
        return dns.resolver.Resolver()

    def get_root_server_ips(self,sys_resolver):
        """
        Using the sys-resolver setup in the constructor to get the IP addresses of the root-servers
        :param sys_resolver:
        :return:
        List of rootserver objects that has IPs
        """
        ROOTSERVER_ADDR = [sys_resolver.query(server).rrset for server in myDig._STATIC_ROOT_SERVER_NAMES]
        return ROOTSERVER_ADDR

    def dig_query(self, url, rtype, name_servers):
        """
        Dig Query sectio, that does a single level of querying on an url,
        of a certain record type, on a set of name servers
        :param url string: domain-name
        :param rtype string: query type
        :param name_servers list[obj]: List of name servers
        :return:
        """
        ## Creating appropriate Query
        domain_name = dns.name.from_text(url)
        query_exp = dns.message.make_query(domain_name, rtype)

        for root_server in name_servers:

            if root_server.items[0].rdtype == dns.rdatatype.A:
                try:
                    response = dns.query.udp(query_exp, root_server.items[0].address)
                    if  not (len(response.answer) == 0 and
                             len(response.additional) == 0 and
                             len(response.authority) == 0):
                        return response

                except Exception as e:
                    print(e + "Server " + root_server.items[0].address + "unavailable! Moving to next...")
                    continue

    def dig_search(self, url, rtype):
        tld_nameservers = self.dig_query(url, rtype, self.root_server_addresses)
        local_nameservers = self.dig_query(url, rtype, tld_nameservers.additional)
        if len(local_nameservers.additional) > 0:
            response = self.dig_query(url,rtype,local_nameservers.additional)
            return response.answer
        else:
            url_new = str(local_nameservers.authority[0].items[0].target)
            tld_servers = self.dig_query(url_new, rtype, self.root_server_addresses)
            local_nameservers = self.dig_query(url_new, rtype, tld_servers.additional)
            response = self.dig_query(url, rtype, local_nameservers.additional)
            if len(response.authority) > 0:
                return response.authority
            return response.answer

    def dig(self,url,rtype):
        print('QUESTION SECTION:')
        print("%s \t IN \t %s \n" %(url,rtype))
        print("ANSWER SECTION:")
        response = self.dig_search(url,rtype)
        for record in response:
             print(record.to_text())
        #print(response[0])

if __name__ == '__main__':

    domain_name = str(sys.argv[1])
    qtype = str(sys.argv[2])
    start_time = time.time()
    d = myDig()
    d.dig(domain_name, qtype)
    end_time = time.time()
    print("\nTime elapsed: %s ms." % str((end_time - start_time)))

