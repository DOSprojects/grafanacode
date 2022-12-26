# c_colors.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
'''
    grafanacode: Grafana color names.
    See `createVisualizationColors.ts <https://github.com/grafana/grafana/blob/main/packages/grafana-data/src/themes/createVisualizationColors.ts>`_

    Use::

        import c_colors as COLORS
        fcolor='TRANSP'

        in resolve:
            import c_colors as COLORS
            fcolor=COLORS['transp']['dark']
'''

#******************************************************************************
# EXTERNAL MODULE REFERENCES
#******************************************************************************
from attrs           import define, field, Factory
from attr.validators import in_, instance_of, optional, deep_iterable

#******************************************************************************
# COLORS
#******************************************************************************
DASHBOARDSTYLES = ['dark', 'light']

COLORS = {
    'TRANSP'       : {'dark': '#000000', 'light': '#000000', 'name': 'transparent'},
    'TEXT'         : {'dark': '#CCCCDC', 'light': '#000000', 'name': 'text'},
    'BLACK'        : {'dark': '#000000', 'light': '#000000', 'name': ''},               #black
    'WHITE'        : {'dark': '#FFFFFF', 'light': '#FFFFFF', 'name': ''},               #white
    'SL_GREY'      : {'dark': '#E0E0E0', 'light': '#E0E0E0', 'name': ''},               #dark-grey
    'L_GREY'       : {'dark': '#B0B0B0', 'light': '#B0B0B0', 'name': ''},               #semi-dark-grey
    'GREY'         : {'dark': '#909090', 'light': '#909090', 'name': ''},               #grey
    'SD_GREY'      : {'dark': '#606060', 'light': '#606060', 'name': ''},               #light-grey
    'D_GREY'       : {'dark': '#303030', 'light': '#303030', 'name': ''},               #super-light-grey
    'SL_RED'       : {'dark': '#FFA6B0', 'light': '#FF7383', 'name': 'super-light-red'},
    'L_RED'        : {'dark': '#FF7383', 'light': '#F2495C', 'name': 'light-red'},
    'RED'          : {'dark': '#F2495C', 'light': '#E02F44', 'name': 'red'},
    'SD_RED'       : {'dark': '#E02F44', 'light': '#C4162A', 'name': 'semi-dark-red'},
    'D_RED'        : {'dark': '#C4162A', 'light': '#AD0317', 'name': 'dark-red'},
    'SL_ORANGE'    : {'dark': '#FFCB7D', 'light': '#FFB357', 'name': 'super-light-orange'},
    'L_ORANGE'     : {'dark': '#FFB357', 'light': '#FF9830', 'name': 'light-orange'},
    'ORANGE'       : {'dark': '#FF9830', 'light': '#FF780A', 'name': 'orange'},
    'SD_ORANGE'    : {'dark': '#FF780A', 'light': '#FA6400', 'name': 'semi-dark-orange'},
    'D_ORANGE'     : {'dark': '#FA6400', 'light': '#E55400', 'name': 'dark-orange'},
    'SL_YELLOW'    : {'dark': '#FFF899', 'light': '#FFEE52', 'name': 'super-light-yellow'},
    'L_YELLOW'     : {'dark': '#FFEE52', 'light': '#FADE2A', 'name': 'light-yellow'},
    'YELLOW'       : {'dark': '#FADE2A', 'light': '#F2CC0C', 'name': 'yellow'},
    'SD_YELLOW'    : {'dark': '#F2CC0C', 'light': '#E0B400', 'name': 'semi-dark-yellow'},
    'D_YELLOW'     : {'dark': '#E0B400', 'light': '#CC9D00', 'name': 'dark-yellow'},
    'SL_GREEN'     : {'dark': '#C8F2C2', 'light': '#96D98D', 'name': 'super-light-green'},
    'L_GREEN'      : {'dark': '#96D98D', 'light': '#73BF69', 'name': 'light-green'},
    'GREEN'        : {'dark': '#73BF69', 'light': '#56A64B', 'name': 'green'},
    'SD_GREEN'     : {'dark': '#56A64B', 'light': '#37872D', 'name': 'semi-dark-green'},
    'D_GREEN'      : {'dark': '#37872D', 'light': '#19730E', 'name': 'dark-green'},
    'SL_BLUE'      : {'dark': '#C0D8FF', 'light': '#8AB8FF', 'name': 'super-light-blue'},
    'L_BLUE'       : {'dark': '#8AB8FF', 'light': '#5794F2', 'name': 'light-blue'},
    'BLUE'         : {'dark': '#5794F2', 'light': '#3274D9', 'name': 'blue'},
    'SD_BLUE'      : {'dark': '#3274D9', 'light': '#1F60C4', 'name': 'semi-dark-blue'},
    'D_BLUE'       : {'dark': '#1F60C4', 'light': '#1250B0', 'name': 'dark-blue'},
    'SL_PURPLE'    : {'dark': '#DEB6F2', 'light': '#CA95E5', 'name': 'super-light-purple'},
    'L_PURPLE'     : {'dark': '#CA95E5', 'light': '#B877D9', 'name': 'light-purple'},
    'PURPLE'       : {'dark': '#B877D9', 'light': '#A352CC', 'name': 'purple'},
    'SD_PURPLE'    : {'dark': '#A352CC', 'light': '#8F3BB8', 'name': 'semi-dark-purple'},
    'D_PURPLE'     : {'dark': '#8F3BB8', 'light': '#7C2EA3', 'name': 'dark-purple'},
}

#******************************************************************************
# COLOR JUGGLING
#******************************************************************************
def getColor(color, theme='dark', ashex=True):
    '''
    Function that returns a color.

    If the color is an RGB(A) dataobject, then return its json
    If the color is a color name, just return the name.
    If a hex string was entered, then it remains hex
    If ashex==True, then the color is translated to a hex string.
    If ashex=False and the hex string was found in the color table, then it is translated to a color name.
    Mind that the hex string is theme dependent.

    Parameters:
        color (any): Input color; can be a RGB(A) object, a color name or a hex color string
        theme (string): theme of the dashboard we are in
        ashex (bool): return as a hex string
    Returns:
        any: color
    '''
    # pylint: disable=too-many-branches
    if theme not in ('light', 'dark'):
        raise ValueError(f'Invalid theme {theme} for color {color}')
    if type(color) is RGBA or type(color) is RGB:
        if ashex:
            hcolor = color.toHex()
        else:
            hcolor = color.getJson()
    elif type(color) is str:
        if len(color)<3:
            raise ValueError(f'1 Invalid color {color}')
        if color[0]=='#':                                           # is a hex color
            if ashex:                                               #   we want it as hex
                hcolor = color                                      #      so just return
            else:                                                   #   try to convert to color value
                hcolor = color                                      #      so just return
                # try to convert
        else:                                                       # is a color name
            if color in [sub['name'] for sub in COLORS.values() if 'name' in sub.keys() and sub['name']!='']: # Grafana name
                hcolor = color
            #elif color in COLORS.keys():                     # COLORS name
            elif color in COLORS:                            # COLORS name
                if ashex or COLORS[color]['name']=='':       #   we want it as hex or there is no grafana name
                    hcolor = COLORS[color][theme]
                else:
                    hcolor = COLORS[color]['name']
            else:
                raise ValueError(f'2 Invalid color {color}')
    else:
        raise ValueError(f'3 Invalid color {color}')
    return hcolor

#**********************************************************
@define(slots=False)
class RGBA:
    '''
    Dataclass encapsulating a RGBA value
    '''
    # logging level of this item
    loglevel           : int = 34
    # attributes
    r                  = field( default=0,
                                validator=instance_of(int))
    g                  = field( default=0,
                                validator=instance_of(int))
    b                  = field( default=0,
                                validator=instance_of(int))
    a                  = field( default=0,
                                validator=instance_of(int))

    def toHex(self):
        '''
        Return hex representation of the color.

        Returns:
            string: hex representation of the color
        '''
        return f'#{self.r:02x}{self.g:02x}{self.b:02x}{self.a:02x}'

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this color.

        Parameters:
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        return f'rgba({self.r:02x}{self.g:02x}{self.b:02x}{self.a:02x})'

#**********************************************************
@define(slots=False)
class RGB:
    '''
    Dataclass encapsulating a RGB value
    '''
    # logging level of this item
    loglevel           : int = 34
    # attributes
    r                  = field( default=0,
                                validator=instance_of(int))
    g                  = field( default=0,
                                validator=instance_of(int))
    b                  = field( default=0,
                                validator=instance_of(int))

    def toHex(self):
        '''
        Return hex representation of the color.

        Returns:
            string: hex representation of the color
        '''
        return f'#{self.r:02x}{self.g:02x}{self.b:02x}'

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this color.

        Parameters:
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        return f'rgb({self.r:02x}{self.g:02x}{self.b:02x})'
