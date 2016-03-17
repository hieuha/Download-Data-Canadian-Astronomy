#!/usr/bin/env python
#coding:utf-8
"""
  Author:  HieuHT --<>
  Purpose: Download CSV Data From http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca
  Created: 16/03/2016
"""
import urllib, urllib2
import re
import StringIO
import json
import csv
import pandas as pd
import requests
import os
import optparse

class CanadianAstronomy():
    def __init__(self):
        self.cookie = None
        self.header = {'X-Requested-With': 'XMLHttpRequest',
                       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                       'Referer': 'http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/search/?collection=JCMT&Observation.instrument.name=HARP-ACSIS&Plane.calibrationLevel=0&noexec=true',
                       'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'}
        self.username = None
        self.email = None
        self.root_url = 'http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/AdvancedSearch/package?ID='

    def _post(self, url, data, header):
        post_data = urllib.urlencode(data)
        req = urllib2.Request(url, post_data, headers = header)
        res = urllib2.urlopen(req)
        html = res.read()
        url_location = res.geturl()
        return html, url_location

    def _post_no303(self, url, data, header):
        r = requests.post(url, data, allow_redirects=False, headers = header)
        return r

    def _get(self, url, header):
        req = urllib2.Request(url, headers= header)
        res = urllib2.urlopen(req)
        meta = res.info()
        html = res.read()
        return html, meta

    def _parse_xml(self, xml, tag):
        pattern = r'<%s>(.+?)</%s>' % (tag, tag)
        re_tag = re.search(pattern, xml)
        return re_tag.group(1)

    def _write_file(self, filename, data):
        with open(filename, "w" ) as f:
            f.write(data)
            print 'Downloaded %s' % filename

    #---------------------------------------------------------------------#
    def login(self, username, password):
        url_login = 'http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/ac/login'
        post_login = {'username': username,
                      'password': password}
        try:            
            res_cookie, _ = self._post(url_login, post_login, self.header)
        except:
            print 'Login failed, check your account again!'
            res_cookie = ""
        if username in res_cookie:
            self.username = username
            cookie = 'CADC_SSO="%s"' % res_cookie
            self._write_file('cookie.txt', cookie)
            self.header['Cookie'] = cookie
            return True
        return False

    def whoami(self):
        if self.header.has_key('Cookie'):            
            url_profile = 'http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/ac/users/%s?idType=HTTP' % self.username
            profile, _ = self._get(url_profile, self.header)
            email = self._parse_xml(profile, 'email')
            self.email = email
            print 'Welcome, %s' % email
            return profile
        print 'Cookies is not set! Can not login!'
        return None

    def search(self, parameters):
        url_search = 'http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/AdvancedSearch/find'        
        data = "sort_column=Start+Date&sort_order=descending&formName=adsform&SelectList=Observation.observationURI+AS+%22Preview%22%2C+Observation.target_name+AS+%22Target+Name%22%2C+COORD1(CENTROID(Plane.position_bounds))+AS+%22RA+(J2000.0)%22%2C+COORD2(CENTROID(Plane.position_bounds))+AS+%22Dec.+(J2000.0)%22%2C+Observation.proposal_id+AS+%22Proposal+ID%22%2C+Observation.requirements_flag+AS+%22Quality%22%2C+Plane.time_bounds_cval1+AS+%22Start+Date%22%2C+Observation.sequenceNumber+AS+%22Sequence+Number%22%2C+Observation.instrument_name+AS+%22Instrument%22%2C+Plane.energy_restwav+AS+%22Rest-frame+Energy%22%2C+Plane.energy_transition_species+AS+%22Molecule%22%2C+Plane.energy_transition_transition+AS+%22Transition%22%2C+Plane.energy_bandpassName+AS+%22Filter%22%2C+Plane.time_exposure+AS+%22Int.+Time%22%2C+AREA(Plane.position_bounds)+AS+%22Field+of+View%22%2C+Observation.type+AS+%22Obs.+Type%22%2C+Observation.intent+AS+%22Intent%22%2C+Observation.environment_tau+AS+%22Tau%22%2C+Observation.target_moving+AS+%22Moving+Target%22%2C+Observation.algorithm_name+AS+%22Algorithm+Name%22%2C+Plane.productID+AS+%22Product+ID%22%2C+Plane.dataProductType+AS+%22Data+Type%22%2C+Observation.instrument_keywords+AS+%22Instrument+Keywords%22%2C+Observation.collection+AS+%22Collection%22%2C+Observation.observationID+AS+%22Obs.+ID%22%2C+Plane.calibrationLevel+AS+%22Cal.+Lev.%22%2C+Plane.energy_bounds_cval1+AS+%22Min.+Wavelength%22%2C+Plane.energy_bounds_cval2+AS+%22Max.+Wavelength%22%2C+Observation.proposal_pi+AS+%22P.I.+Name%22%2C+Plane.dataRelease+AS+%22Data+Release%22%2C+Plane.position_sampleSize+AS+%22Pixel+Scale%22%2C+Plane.energy_resolvingPower+AS+%22Resolving+Power%22%2C+Plane.time_bounds_cval2+AS+%22End+Date%22%2C+Plane.provenance_name+AS+%22Provenance+Name%22%2C+Observation.target_type+AS+%22Target+Type%22%2C+Observation.target_standard+AS+%22Target+Standard%22%2C+Observation.proposal_title+AS+%22Proposal+Title%22%2C+Observation.proposal_keywords+AS+%22Proposal+Keywords%22%2C+Plane.position_resolution+AS+%22IQ%22%2C+Plane.energy_emBand+AS+%22Band%22%2C+Plane.provenance_version+AS+%22Prov.+Version%22%2C+Plane.provenance_project+AS+%22Prov.+Project%22%2C+Plane.provenance_runID+AS+%22Prov.+Run+ID%22%2C+Plane.provenance_lastExecuted+AS+%22Prov.+Last+Executed%22%2C+isDownloadable(Plane.planeURI)+AS+%22DOWNLOADABLE%22%2C+Plane.planeURI+AS+%22CAOM+Plane+URI%22&MaxRecords=30000&format=csv&Observation.observationID=&Form.name=Observation.observationID%40Text&Observation.proposal.pi=&Form.name=Observation.proposal.pi%40Text&Observation.proposal.id=&Form.name=Observation.proposal.id%40Text&Observation.proposal.title=&Form.name=Observation.proposal.title%40Text&Observation.proposal.keywords=&Form.name=Observation.proposal.keywords%40Text&Plane.dataRelease=&Form.name=Plane.dataRelease%40TimestampFormConstraint&Form.name=Plane.dataRelease%40PublicTimestampFormConstraint&Observation.intent=&Form.name=Observation.intent%40Text&Plane.position.bounds%40Shape1Resolver.value=ALL&Plane.position.bounds%40Shape1.value=&targetList=&Form.name=targetList.targetList&Form.name=Plane.position.bounds%40Shape1&Plane.position.sampleSize=&Form.name=Plane.position.sampleSize%40Number&Form.name=Plane.position.DOWNLOADCUTOUT%40Boolean&Plane.time.bounds%40Date.value=&Plane.time.bounds_PRESET%40Date.value=&Form.name=Plane.time.bounds%40Date&Plane.time.exposure=&Form.name=Plane.time.exposure%40Number&Plane.time.bounds.width=&Form.name=Plane.time.bounds.width%40Number&Plane.energy.bounds%40Energy.value=AAAAAAA1&Form.name=Plane.energy.bounds%40Energy&Plane.energy.sampleSize=&Form.name=Plane.energy.sampleSize%40Number&Plane.energy.resolvingPower=&Form.name=Plane.energy.resolvingPower%40Number&Plane.energy.bounds.width=&Form.name=Plane.energy.bounds.width%40Number&Plane.energy.restwav=&Form.name=Plane.energy.restwav%40Number&Form.name=Plane.energy.DOWNLOADCUTOUT%40Boolean&Form.name=Plane.energy.emBand%40Enumerated&Form.name=Observation.collection%40Enumerated&Form.name=Observation.instrument.name%40Enumerated&Form.name=Plane.energy.bandpassName%40Enumerated&Form.name=Plane.calibrationLevel%40Enumerated&Form.name=Plane.dataProductType%40Enumerated&Form.name=Observation.type%40Enumerated&Observation.collection=AAAAAAA2&Observation.instrument.name=AAAAAAA3&Plane.energy.bandpassName=&Plane.calibrationLevel=0&Plane.dataProductType=&Observation.type="
        data = data.replace('AAAAAAA1', parameters['energy_value'])
        data = data.replace('AAAAAAA2', parameters['collection'])
        data = data.replace('AAAAAAA3', parameters['instrument_name'])

        r = self._post_no303(url_search, data, self.header)
        url_job = r.headers['Location']
        search_result_html, _ = self._get(url_job, self.header)
        search_result_html = StringIO.StringIO(search_result_html)
        search_result_json = json.load(search_result_html)
        run_id = search_result_json['run_id']
        print 'Fetching Data From #JobID: %s' % run_id
        results_url = search_result_json['results_url']
        html, meta = self._get(results_url, self.header)
        filename = 'result_%s.csv' % run_id
        self._write_file(filename, html)
        return filename

#---------------------------------------------------------------------#
def group_resolving_power(x):
    if 300000.0 <= x['Resolving Power'] <= 399999.0:    
        return str(300000)
    elif 700000.0 <= x['Resolving Power'] <= 799999.0:
        return str(700000)
    elif 5000000.0 <= x['Resolving Power'] <= 5999999.0:        
        return str(5000000)
    elif 10000000.0 <= x['Resolving Power'] <= 19999999.0:
        return str(10000000)  
    return str(x['Resolving Power'])

def build_parser():
    usage = """
    usage: %prog -s 192.168.12.20 -p 6379 -w 20 -c 30 -a foobared -t 2000
    -u: username
    -p: password
    -e: energy value, eg: "356700..356800MHz"
    -i: instrument name, eg: HARP-ACSIS
    -c: collection, eg: JCMT
    """    
    parser = optparse.OptionParser(usage= usage)
    parser.add_option("-u", "--username", dest="username")
    parser.add_option("-p", "--password", dest="password")
    parser.add_option("-e", "--engery", dest="engery", default = "356700..356800MHz")
    parser.add_option("-i", "--instrument", dest="instrument", default = "HARP-ACSIS")
    parser.add_option("-c", "--collection", dest="collection", default="JCMT")
    return parser

def main():
    parser = build_parser()
    options, _args = parser.parse_args()
    username = options.username
    password = options.password
    collection = options.collection
    instrument = options.instrument
    engery = options.engery
    parameters = {'energy_value': engery,
                  'instrument_name': instrument,
                  'collection': collection}
    if not options.username:
        parser.error("Username is required")
    if not options.password:
        parser.error("Password is required")
        
    ca = CanadianAstronomy()
    if ca.login(username, password):
        ca.whoami()        
        saved_file = ca.search(parameters)

        # Processing CSV file downloaded
        data = pd.DataFrame.from_csv(saved_file)
        data['DOWNLOADABLE'] = ca.root_url + data['DOWNLOADABLE'].astype(str)        
        data['Resolving Power Group'] = data.apply (lambda row: group_resolving_power (row),axis=1)
        select_conditional = ['Target Name', 'Molecule', 'Transition', 'Resolving Power Group']
        grouped =  data.groupby(select_conditional)
        for group_name, df in grouped:
            group_name_friendly = '_'.join(group_name).replace(' ', '') 
            if not os.path.isdir(group_name_friendly):
                os.makedirs(group_name_friendly)
                print 'Created directory %s' % group_name_friendly
            path_file = group_name_friendly + '/' + group_name_friendly
            with open(path_file + '.csv', 'w') as f:
                df.to_csv(f)
            with open(path_file + '.links' , 'w') as f2:
                df['DOWNLOADABLE'].to_csv(f2, index=False)

if __name__ == "__main__":
   
        
    main()

