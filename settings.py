INFLUX_HOST = "45.32.61.92"
INFLUX_PORT = 8086
INFLUX_USER = None
INFLUX_PASSWORD = None
INFLUX_DB = "datadog"

STOCK_METRICS = {"cpuSystem": "cpu.System",
                 "cpuUser": "cpu.User",
                 "cpuGuest": "cpu.Guest",
                 "cpuStolen": "cpu.Stolen",
                 "cpuWait": "cpu.Wait",
                 "cpuIdle": "cpu.Idle",
                 "memShared": "mem.Shared",
                 "memPhysUsable": "mem.Phys_Usable",
                 "memPhysFree": "mem.Phys_Free",
                 "memPhysTotal": "mem.Phys_Total",
                 "memPhysUsed": "mem.Phys_Used",
                 "memPhysPctUsable": "mem.Phys.Pct.Usable",
                 "memPageTables": "mem.Page_Tables",
                 "memCached": "mem.Cached",
                 "memSwapTotal": "mem.Swap_Total",
                 "memSwapCached": "mem.Swap_Cached",
                 "memSwapFree": "mem.Swap_Free",
                 "memSwapUsed": "mem.Swap_Used",
                 "memSwapPctFree": "mem.Swap.Pct.Free",
                 "memBuffers": "mem.Buffers",
                 "memSlab": "memSlab",
                 "system.load.norm.1": "system.load.norm.1",
                 "system.load.norm.5": "system.load.norm.5",
                 "system.load.norm.15": "system.load.norm.15",
                 "system.load.1": "system.load.1",
                 "system.load.5": "system.load.5",
                 "system.load.15": "system.load.15",
                 "system.uptime": "system.uptime",
                 }
