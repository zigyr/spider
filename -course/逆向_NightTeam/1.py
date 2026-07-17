# 长期使用
import os
os.environ["EXECJS_RUNTIME"] = "Node"

# 临时使用
import execjs.runtime_names
node = execjs.get(execjs.runtime_names.Node)