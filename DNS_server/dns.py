from cache import Cache
from dnslib import DNSRecord, RCODE
import socket

TRUST_SERVER = "77.88.8.1"


class DNS:
    def __init__(self):
        self.cache = Cache()
        self.cache.load_cache("cache")

    def process(self, query):
        try:
            query = DNSRecord.parse(query)
            query_key = (query.q.qtype, query.q.qname)
            rdata = self.cache.get_cache(query_key)
            if rdata:
                response = DNSRecord(header=query.header)
                response.add_question(query.q)
                response.rr.extend(rdata)
                print(f"Найденые записи в кэше:\n{response}",
                      end="\n\n")
                return response.pack()

            response = query.send(TRUST_SERVER, 53, timeout=5)
            response = DNSRecord.parse(response)

            # Проверка ответа
            if response.header.rcode != RCODE.NOERROR:
                raise Exception(f"Ошибка ответа: {response.header.rcode}")
            if not response.questions or not response.rr:
                raise Exception("Неверный ответ")

            # Обновление кэша
            records_by_type = {}
            for rr_section in (
                    response.rr, response.auth,
                    response.ar):
                for rr in rr_section:
                    if (rr.rtype, rr.rname) not in records_by_type:
                        records_by_type[(rr.rtype, rr.rname)] = []
                    records_by_type[(rr.rtype, rr.rname)].append(rr)
            for key, records in records_by_type.items():
                self.cache.update_cache(key, records, records[0].ttl)

            return response.pack()
        except Exception as e:
            print(f"Ошибка DNS: {e}")
            return None
        except socket.error as e:
            print(f"Ошибка сокета: {e}")
            return None
