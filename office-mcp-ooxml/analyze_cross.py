import json, sys
from pathlib import Path
sys.path.insert(0, '/tmp/office-mcp-ooxml-work/python-office-mcp-server')
from office_server import OfficeServer
s=OfficeServer()
base=Path(__file__).parent/'artifacts'
out={}
for name in ['go_pl.docx','go_pl.xlsx','python_pl.docx','python_pl.xlsx']:
    p=str(base/name)
    out[name]={'read_json': s.tool_office_read(p, output_format='json'), 'read_markdown': s.tool_office_read(p, output_format='markdown')[:2000]}
    try: out[name]['inspect']=s.tool_office_inspect(p, what='structure')
    except Exception as e: out[name]['inspect_error']=repr(e)
print(json.dumps(out, indent=2, default=str)[:20000])
