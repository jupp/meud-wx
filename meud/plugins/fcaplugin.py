"""FCA plugin"""
import os.path

import wx

import fca

from _plugin import Plugin

class FCAPlugin(Plugin):
    name = "FCA"
    
    def get_actions(self, item):
        if item.type == "Context":
            return ["Save concepts"]
        if item.type == "Many-valued context":
            return ["Scale"]
    
    def do_action(self, item, action):
        if action == "Save concepts":
            return self.SaveConcepts(item)
        elif action == "Scale":
            return self.ScaleMVContext(item)
        
    def ScaleMVContext(self, item):
        mvcontext = fca.read_mv_txt(item.path)
        
        
    def SaveConcepts(self, item):
        (root, ext) = os.path.splitext(item.name)
        if ext == ".cxt":
            cxt = fca.read_cxt(item.path)
        elif ext == ".txt":
            cxt = fca.read_txt(item.path)
        cs = fca.norris(cxt)
        number_of_concepts = len(cs)
    
        default_path = "".join([item.path[:-3], "xml"])
        newpath = default_path
        i = 1
        while (os.path.exists(newpath)):
            newpath = default_path[:-4] + "-{0}".format(i) + newpath[-4:]
            i += 1
        fca.write_xml(newpath, cs)
            
        dlg = wx.MessageDialog(None, str(number_of_concepts) +\
                                " concepts have been stored in " + newpath,
                                "Done",
                                wx.OK | wx.ICON_INFORMATION
                                )
        dlg.ShowModal()
        dlg.Destroy()
        
        return [newpath]