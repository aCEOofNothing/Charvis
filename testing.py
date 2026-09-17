from assets import import_data

def load_plugins():
        plugin_list = import_data("core_py_plugins/plugin-list.json")
        import core_py_plugins
        return plugin_list

plugin_list = load_plugins()
for keyword, name in plugin_list.items():
        name()