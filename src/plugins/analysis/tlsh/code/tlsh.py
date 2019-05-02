from analysis.PluginBase import AnalysisBasePlugin
from helperFunctions.hash import get_tlsh_compairson
from storage.db_interface_common import MongoInterfaceCommon
from helperFunctions.web_interface import ConnectTo


class AnalysisPlugin(AnalysisBasePlugin):
    '''
    TLSH Plug-in
    '''
    NAME = 'tlsh'
    DESCRIPTION = 'find files with similar tlsh and calculate similarity value'
    DEPENDENCIES = ['file_hashes']
    VERSION = '0.1'

    def __init__(self, plugin_adminstrator, config=None, recursive=True):
        super().__init__(plugin_adminstrator, config=config, recursive=recursive, plugin_path=__file__)

    def process_object(self, file_object):

        comparisons_dict = {}

        if 'tlsh' in file_object.processed_analysis['file_hashes'].keys():

            comparisons_dict = {}

            with ConnectTo(TLSHInterface, self.config) as interface:

                for file in interface.tlsh_query_file_object(file_object):

                    value = get_tlsh_compairson(file_object.processed_analysis['file_hashes']['tlsh'],
                                                file['processed_analysis']['file_hashes']['tlsh'])
                    if value <= 150 and not file['_id'] == file_object.get_uid():
                        comparisons_dict[file['_id']] = value

        file_object.processed_analysis[self.NAME] = comparisons_dict

        return file_object


class TLSHInterface(MongoInterfaceCommon):
    READ_ONLY = True

    def tlsh_query_file_object(self, file_object):
        return self.file_objects.find({"processed_analysis.file_hashes.tlsh": {"$exists": True}})

    def tlsh_query_firmware_collection(self, firmware):
        return self.firmwares.find({"processed_analysis.file_hashes.tlsh": {"$exists": True}})
