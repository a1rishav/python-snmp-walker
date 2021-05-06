from easysnmp import Session
from pysnmp.smi import builder, view, compiler

class SnmpAgent:

    def __init__(self, hostname, snp_version=2):
        self.hostname = hostname
        self.snp_version = snp_version
        self.session = self.get_session()
        
    def get_session(self):
        return Session(hostname=self.hostname, community='public', version=self.snp_version)
    
    def get_objects_from_snmp_walk(self, base_oid_str):
        return self.session.walk(base_oid_str)
    
    def print_snmp_walk_objects(self, objects):
        for item in objects:
            print('{oid}.{oid_index} {snmp_type} = {value}'.format(
                oid=item.oid,
                oid_index=item.oid_index,
                snmp_type=item.snmp_type,
                value=item.value
            ))
    
    def create_mib_viewer(self, mib_name, mib_path_dir='/usr/share/snmp/mibs'):
        mibBuilder = builder.MibBuilder()
        compiler.addMibCompiler(mibBuilder, sources=[mib_path_dir])
        mibBuilder.loadModules(mib_name)
        mib_viewer = view.MibViewController(mibBuilder)
        return mib_viewer

    def get_name_from_snmp_object_oid(self, mib_viewer, oid_string):
        '''
        :param mib_viewer: object from create_mib_viewer()
        :param oid_string: format example : 1.3.6.1.2.1.1.6.0
        :return:
        '''
        oid_tuples = tuple([int(oid_val) for oid_val in oid_string.split(".")])
        return mib_viewer.getNodeNameByOid(oid_tuples)[1][-1]

if __name__ == '__main__':
    agent = SnmpAgent(hostname="localhost")

    # uptime
    objs = agent.get_objects_from_snmp_walk(base_oid_str="iso.3.6.1.2.1.1.9.1.3")
    mib_viewer = agent.create_mib_viewer(mib_name="IF-MIB")

    for obj in objs:
        # if snmp walk returns objects in format iso.3.6.1, iso needs to be converted to 1
        # use a mapping dict to convert this
        obj_oid = obj.oid.replace("iso", "1")
        obj_name = agent.get_name_from_snmp_object_oid(mib_viewer, obj_oid)
        print("{} : {}".format(obj_name, obj.value))
        '''
        Sample output :
        sysORDescr : The MIB for Message Processing and Dispatching.
        sysORDescr : The management information definitions for the SNMP User-based Security Model.
        sysORDescr : The SNMP Management Architecture MIB.
        sysORDescr : The MIB module for SNMPv2 entities
        sysORDescr : View-based Access Control Model for SNMP.
        '''
