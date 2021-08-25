import dns
import dns.resolver
import dns.exception
import dns.edns
import time
import logging


class DNSRequester:
    """ """

    def __init__(self):
        self.res = dns.resolver.Resolver()
        self.res.timeout = 3
        self.res.nameservers = [self.res.nameservers[0]]
        self.options = None
        self.option_ecs = None

    def setServer(self, server):
        """change the DNS server"""
        self.res.nameservers = [server]

    def setTimeout(self, timeout):
        """change the DNS server timeout"""
        self.res.timeout = timeout

    def addOptionIPAddressECS(self, ip):
        self.options = dns.edns.ECSOption.from_text('{}/32'.format(ip))
        self.option_ecs = ip

    def _request(self, qname, rdtype="A"):
        """ unit dns request"""

        cache = dns.resolver.Cache()
        cache.flush()

        r = {
            'dns-error': 'no-error',
            'dns-server': self.res.nameservers[0],
            'dns-target': str(qname),
            'dns-rdtype': str(rdtype),
            'dns-proto': "UDP"
        }

        if self.option_ecs:
            r['client-ip'] = self.option_ecs

        try:
            now = time.time()

            message = dns.message.make_query(qname=qname,
                                             rdtype=rdtype,
                                             options=self.options)

            myAnswers = dns.query.udp(message,
                                      self.res.nameservers[0])

            # print(myAnswers.rcode())
            # print(type(myAnswers.resolve_chaining().answer.to_rdataset()))
            # print(myAnswers.resolve_chaining().answer.to_rdataset().rdtype)

            r['dns-response-time'] = float((time.time() -
                                            now).__format__('0.5f'))

            if myAnswers.rcode() != dns.rcode.NOERROR:
                r['dns-error'] = dns.rcode.to_text(myAnswers.rcode())
            else:
                r['dns-ttl'] = myAnswers.resolve_chaining().minimum_ttl
                r['dns-canonical'] = str(myAnswers.canonical_name())
                r['dns-response'] = str(myAnswers.resolve_chaining().answer[0])

        # except dns.resolver.NoNameservers:
        #     r['dns-error'] = "no name servers"
        # except dns.exception.Timeout:
        #     r['dns-error'] = "timeout"
        # except dns.resolver.NoAnswer:
        #     r['dns-error'] = "no answer"
        # except dns.resolver.NXDOMAIN:
        #     r['dns-error'] = "name does not exist"
        # except dns.exception.DNSException:
        #     r['dns-error'] = "unknown"

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)
            exit()

        return r

    def simple(self, qname):
        """makes a simple A request on the fqdn"""
        r = self._request(qname)
        return r

    def __str__(self):
        r = "DNS Resolver: srv={}".format(self.res.nameservers[0])
        if self.option_ecs:
            r += " ECS={}/32".format(self.option_ecs)
        r += " timeout={}s".format(self.res.timeout)

        return r
