# c_units.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
'''
    grafanacode: Grafana unit formats.
    See `categories.ts <https://github.com/grafana/grafana/blob/main/packages/grafana-data/src/valueFormats/categories.ts>`_

    Use::

        import c_units as UNITS
        units=UNITS.nG_P_NORMAL_M3
'''

#******************************************************************************
# EXTERNAL MODULE REFERENCES
#******************************************************************************

#******************************************************************************
# UNIT FORMATS
#******************************************************************************
NOFORMAT        = 'none'
NUMBER          = 'none'
STRING          = 'string'
PERCENT         = 'percent'
PERCENTUNIT     = 'percentunit'
SHORT           = 'short'
HEX             = 'hex'
HEXOX           = 'hex0x'           # 0x
SCIENTIFIC      = 'sci'
LOCALE          = 'locale'

PIXELS          = 'pixel'
HUMIDITY        = 'humidity'        # %H
DECIBEL         = 'dB'
# Acceleration
M_P_S2          = 'accMS2'          # m/sec²
FT_P_S2         = 'accFS2'          # f/sec²
G               = 'accG'            # g
# Angle
DEG             = 'degree'          # °
RAD             = 'radian'          # rad
GRAD            = 'grad'            # grad
ARCMIN          = 'arcmin'          # arcmin
ARCSEC          = 'arcsec'          # arcsec
# Area
M2              = 'areaM2'          # m²
FT2             = 'areaF2'          # ft²
MI2             = 'areaMI2'         # mi²
# Computation
FLOPS_P_S       = 'flops'           # FLOP/s
MFLOPS_P_S      = 'mflops'          # MFLOP/s
GFLOPS_P_S      = 'gflops'          # GFLOP/s
TFLOPS_P_S      = 'tflops'          # TFLOP/s
PFLOPS_P_S      = 'pflops'          # PFLOP/s
EFLOPS_P_S      = 'eflops'          # EFLOP/s
ZFLOPS_P_S      = 'zflops'          # ZFLOP/s
YFLOPS_P_S      = 'yflops'          # YFLOP/s
# Concentration
PPM             = 'ppm'             # ppm
PPB             = 'conppb'          # ppb
nG_P_M3         = 'conngm3'         # ng/m³
nG_P_NORMAL_M3  = 'conngNm3'        # ng/Nm³
uG_P_M3         = 'conμgm3'         # μg/m³
uG_P_NORMAL_M3  = 'conμgNm3'        # μg/Nm³
mG_P_M3         = 'conmgm3'         # mg/m³
mG_P_NORMAL_M3  = 'conmgNm3'        # mg/Nm³
G_P_M3          = 'congm3'          # g/m³
G_P_NORMAL_M3   = 'congNm3'         # g/Nm³
mG_P_DL         = 'conmgdL'         # mg/dL
mMOL_P_L        = 'conmmolL'        # mmol/L
# Currency
DOLLAR                  = 'currencyUSD' # $
POUND                   = 'currencyGBP' # £
EURO                    = 'currencyEUR' # €
YEN                     = 'currencyJPY' # ¥
RUBLES                  = 'currencyRUB' # ₽
HRYVNIAS                = 'currencyUAH' # ₴
REAL                    = 'currencyBRL' # R$
DANISH_KRONE            = 'currencyDKK' # kr
ICELANDIC_KRONA         = 'currencyISK' # kr
NORWEGIAN_KRONE         = 'currencyNOK' # kr
SWEDISH_KORNA           = 'currencySEK' # kr
CZECH_KORUNA            = 'currencyCZK' # czk
SWISS_FRANC             = 'currencyCHF' # CHF
POLISH_ZLOTY            = 'currencyPLN' # PLN
BITCOIN                 = 'currencyBTC' # ฿
MILLI_BITCOIN           = 'currencymBTC'    # mBTC
MICRO_BITCOIN           = 'currencyμBTC'    # μBTC
SOUTH_AFRICAN_RAND      = 'currencyZAR' # R
INDIAN_RUPEE            = 'currencyINR' # ₹
SOUTH_KOREAN_WON        = 'currencyKRW' # ₩
INDONESIAN_RUPIAH       = 'currencyIDR' # Rp
PHILIPPINE_PESO         = 'currencyPHP' # PHP
# Data
BYTES_IEC       = 'bytes'
BYTES           = 'decbytes'    # B
BITS_IEC        = 'bits'
BITS            = 'decbits'
KIBI_BYTES      = 'kbytes'      # KiB
KILO_BYTES      = 'deckbytes'   # kB
MEBI_BYTES      = 'mbytes'      # MiB
MEGA_BYTES      = 'decmbytes'   # MB
GIBI_BYTES      = 'gbytes'      # GiB
GIGA_BYTES      = 'decgbytes'   # GB
TEBI_BYTES      = 'tbytes'      # TiB
TERA_BYTES      = 'dectbytes'   # TB
PEBI_BYTES      = 'pbytes'      # PiB
PETA_BYTES      = 'decpbytes'   # PB
# Data Rate
PACKETS_P_S     = 'pps'         # p/s

BYTES_P_S_IEC   = 'binBps'      # B/s
KIBI_BYTES_P_S  = 'KiBs'        # KiB/s
MEBI_BYTES_P_S  = 'MiBs'        # MiB/s
GIBI_BYTES_P_S  = 'GiBs'        # GiB/s
TEBI_BYTES_P_S  = 'TiBs'        # TiB/s
PEBI_BYTES_P_S  = 'PiBs'        # PB/s

BYTES_P_S       = 'Bps'         # B/s
KILO_BYTES_P_S  = 'KBs'         # kB/s
MEGA_BYTES_P_S  = 'MBs'         # MB/s
GIGA_BYTES_P_S  = 'GBs'         # GB/s
TERA_BYTES_P_S  = 'TBs'         # TB/s
PETA_BYTES_P_S  = 'PBs'         # PB/s

BITS_P_S_IEC    = 'binbps'      # b/s
KIBI_BITS_P_S   = 'Kibits'      # Kib/s
MEBI_BITS_P_S   = 'Mibits'      # Mib/s
GIBI_BITS_P_S   = 'Gibits'      # Gib/s
TEBI_BITS_P_S   = 'Tibits'      # Tib/s
PEBI_BITS_P_S   = 'Pibits'      # Pib/s

BITS_P_S        = 'bps'         # b/s
KILO_BITS_P_S   = 'Kbits'       # kb/s
MEGA_BITS_P_S   = 'Mbits'       # Mb/s
GIGA_BITS_P_S   = 'Gbits'       # Gb/s
TERA_BITS_P_S   = 'Tbits'       # Tb/s
PETA_BITS_P_S   = 'Pbits'       # Pb/s
# Date & Time
DATETIME_ISO            = 'dateTimeAsIso'
DATETIME_ISO_TODAY      = 'dateTimeAsIsoNoDateIfToday'
DATETIME_US             = 'dateTimeAsUS'
DATETIME_US_TODAY       = 'dateTimeAsUSNoDateIfToday'
DATETIME_LOCAL          = 'dateTimeAsLocal'
DATETIME_LOCAL_TODAY    = 'dateTimeAsLocalNoDateIfToday'
DATETIME_DEFAULT        = 'dateTimeAsSystem'
DATETIME_FROM_NOW       = 'dateTimeFromNow'
# Energy
W               = 'watt'            # W
KW              = 'kwatt'           # kW
MW              = 'megwatt'         # MW
GW              = 'gwatt'           # GW
mM              = 'mwatt'           # mW
W_P_M2          = 'Wm2'             # W/m²
VA              = 'voltamp'         # VA
KVA             = 'kvoltamp'        # kVA
VAR             = 'voltampreact'    # VAR
KVAR            = 'kvoltampreact'   # kVAR
W_HOUR          = 'watth'           # Wh
W_HOUR_KILO     = 'watthperkg'      # Wh/kg
KWH             = 'kwatth'          # kWh
KWMIN           = 'kwattm'          # kWm
AMP_HOUR        = 'amph'            # Ah
KAMP_HOUR       = 'kamph'           # kAh
mAMP_HOUR       = 'mamph'           # mAh
JOULE           = 'joule'           # J
EV              = 'ev'              # eV
AMP             = 'amp'             # A
KAMP            = 'kamp'            # kA
mAMP            = 'mamp'            # mA
V               = 'volt'            # V
KV              = 'kvolt'           # kV
mV              = 'mvolt'           # mV
DB_mW           = 'dBm'             # dBm
OHM             = 'ohm'             # Ω
KOHM            = 'kohm'            # kΩ
MOHM            = 'Mohm'            # MΩ
F               = 'farad'           # F
uF              = 'µfarad'          # µF
nF              = 'nfarad'          # nF
pF              = 'pfarad'          # pF
fF              = 'ffarad'          # fF
H               = 'henry'           # H
mH              = 'mhenry'          # mH
uH              = 'µhenry'          # µH
LM              = 'lumens'          # Lm
# Flow
GALLONS_P_MIN   = 'flowgpm'         # gpm
M3_P_S          = 'flowcms'         # cms
FT3_P_S         = 'flowcfs'         # cfs
FT3_P_MIN       = 'flowcfm'         # cfm
L_P_HOUR        = 'litreh'          # L/h
L_P_MIN         = 'flowlpm'         # L/min
mL_P_MIN        = 'flowmlpm'        # mL/min
LUX             = 'lux'             # lx
# Force
NM              = 'forceNm'         # Nm
KNM             = 'forcekNm'        # kNm
N               = 'forceN'          # N
KN              = 'forcekN'         # kN
# Hash Rate
HASHES_P_S      = 'Hs'              # H/s
KHASHES_P_S     = 'KHs'             # kH/s
MHASHES_P_S     = 'MHs'             # MH/s
GHASHES_P_S     = 'GHs'             # GH/s
THASHES_P_S     = 'THs'             # TH/s
PHASHES_P_S     = 'PHs'             # PH/s
EHASHES_P_S     = 'EHs'             # EH/s
# Mass
mG              = 'massmg'          # mg
G               = 'massg'           # g
LB              = 'masslb'          # lb
KG              = 'masskg'          # kg
TON             = 'masst'           # t
# Length
mM              = 'lengthmm'        # mm
IN              = 'lengthin'        # in
M               = 'lengthm'         # m
KM              = 'lengthkm'        # km
FT              = 'lengthft'        # ft
MI              = 'lengthmi'        # mi
# Pressure
mBAR            = 'pressurembar'    # mBar,
BAR             = 'pressurebar'     # Bar,
KBAR            = 'pressurekbar'    # kBar,
PA              = 'pressurepa'      # Pa
HPA             = 'pressurehpa'     # hPa
KPA             = 'pressurekpa'     # kPa
HG              = 'pressurehg'      # "Hg
PSI             = 'pressurepsi'     # psi
# Radiation
BECQUEREL       = 'radbq'           # Bq
CURIE           = 'radci'           # Ci
RAD_GRAY        = 'radgy'           # Gy
RAD_RAD         = 'radrad'          # rad
uSIEVERT        = 'radusv'          # µSv
mSIEVERT        = 'radmsv'          # mSv
SIEVERT         = 'radsv'           # Sv
REM             = 'radrem'          # rem
EXPOSURE        = 'radexpckg'       # C/kg
ROENTGEN        = 'radr'            # R
uSIEVERT_P_HOUR = 'radusvh'         # µSv/h
mSIEVERT_P_HOUR = 'radmsvh'         # mSv/h
SIEVERT_P_HOUR  = 'radsvh'          # Sv/h
# Rotational Speed
RPM             = 'rotrpm'          # rpm
ROT_HZ          = 'rothz'           # Hz
RAD_P_S         = 'rotrads'         # rad/s
DEG_P_S         = 'rotdegs'         # °/s
# Temperature
CELSIUS         = 'celsius'         # °C
FAHRENHEIT      = 'fahrenheit'      # °F
KELVIN          = 'kelvin'          # K
# Time
HZ              = 'hertz'           # Hz
nS              = 'ns'              # ns
uS              = 'µs'              # µs
mM              = 'ms'              # ms
S               = 's'               # s
MIN             = 'm'               # m
HOUR            = 'h'               # h
DAY             = 'd'               # d
DURATION_mS     = 'dtdurationms'    # ms
DURATION_S      = 'dtdurations'     # s
HH_MM_SS        = 'dthms'           # hh:mm:ss
D_HH_MM_SS      = 'dtdhms'          # d hh:mm:ss
TIMETICKS       = 'timeticks'       # s/100
CLOCK_mS        = 'clockms'         # ms
CLOCK_S         = 'clocks'          # s
# Throughput
COUNTS_P_S      = 'cps'             # cps
OPS_P_S         = 'ops'             # ops
REQUESTS_P_S    = 'reqps'           # rps
READS_P_S       = 'rps'             # rps
WRITES_P_S      = 'wps'             # wps
IO_OPS_P_S      = 'iops'            # iops
COUNTS_P_MIN    = 'cpm'             # cpm
OPS_P_MIN       = 'opm'             # opm
READS_P_MIN     = 'rpm'             # rpm
WRITES_P_MIN    = 'wpm'             # wpm
# Velocity
M_P_S           = 'velocityms'      # m/s
KM_P_HOUR       = 'velocitykmh'     # km/h
MI_P_HOUR       = 'velocitymph'     # mph
KNOTS           = 'velocityknot'    # kn
# Volume
mL              = 'mlitre'          # mL
L               = 'litre'           # L
M3              = 'm3'              # m³
NORMAL_M3       = 'Nm3'             # Nm³
dM3             = 'dm3'             # dm³
GALLONS         = 'gallons'         # g
# Boolean
TRUE_FALSE      = 'bool'            # True/False
YES_NO          = 'bool_yes_no'     # Yes/No
ON_OFF          = 'bool_on_off'     # On/Off
