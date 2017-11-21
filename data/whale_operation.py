from .html_helper import get_total_number_of_page,get_html_by_url
from dateutil import parser

def find_whale_tx_helper(url):
    soup = get_html_by_url(url)
    # print(soup)
    if soup is None:
        return []
    trs = soup.findAll("tr")
    tx_arr = []
    for tr_index,tr in enumerate(trs):
        if tr_index != 0:
            # print("tr_index:{}".format(tr_index))
            tds = tr.findAll("td")
            for td_index,td in enumerate(tds):
                if td_index == 1:
                    #timestamp
                    timestamp_s = td.find('span')['title']
                    timestamp = parser.parse(timestamp_s)
                elif td_index == 2:
                    # from_Address
                    m_a = td.find("a")
                    if m_a is None:
                        m_a = td.find("span")
                    from_address = m_a.text
                    # print("from_address:{}".format(from_address))
                elif td_index == 3:
                    # type
                    tx_type = td.find("span").text
                    if "IN" in tx_type:
                        tx_type = "IN"
                    # print("tx_type:{}".format(tx_type))
                elif td_index == 4:
                    # to_Address
                    m_a = td.find("a")
                    if m_a is None:
                        m_a = td.find("span")
                    to_address = m_a.text
                    # print("to_address:{}".format(to_address))
                elif td_index == 5:
                    quantity = float(td.text.replace(",",""))
                    # print("quantity:{}".format(quantity))
            from_address = from_address.lower()
            to_address = to_address.lower()
            tx_arr.append([timestamp,from_address,tx_type,to_address,quantity])
    return tx_arr

def find_whale_txs(token_address,contract_address,start_page=1,end_page=100):
    url = "http://etherscan.io/token/generic-tokentxns2?contractAddress={}&a={}&mode=".format(token_address,contract_address)
    total_number_of_page = get_total_number_of_page(url)
    tx_arrs = []
    print("\t\ttotal_number_of_page:{} for {}".format(total_number_of_page,contract_address))
    end_page = min(total_number_of_page,end_page)
    for i in range(start_page,end_page+1):
        print("\t\t"+str(i))
        tx_arr = find_whale_tx_helper("{}&p={}".format(url,i))
        tx_arrs = tx_arrs + tx_arr
    return tx_arrs

if __name__ == "__main__":
    find_whale_txs('0x255aa6df07540cb5d3d297f0d0d4d84cb52bc8e6','0x8d12a197cb00d4747a1fe03395095ce2a5cc6819',1,5)