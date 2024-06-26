import json

class AppConfig:
    def __init__(self, config_file):
        self.config_file = config_file
        self.default_config = {
            # Simulation Area
            "dimensions": 3,
            "dimX": 500,
            "dimY": 500,
            "dimZ": 500,

            # Simulation
            "asynchronousMode": False, # TODO: implement the ability of 
            "mobility": True, # TODO: implement the ability of mobility
            "interference": True, # TODO: implement the ability of interference
            "interferenceIsAdditive": True, # TODO: implement the ability of interferenceIsAdditive
            "canReceiveWhileSending": True, # TODO: implement the ability of canReceiveWhileSending
            "canReceiveMultiplePacketsInParallel": True, # TODO: implement the ability of canReceiveMultiplePacketsInParallel
            "edge_type": "Edge", # TODO: implement the ability of edge_type
            "exitOnTerminationInGUI": False, # TODO: implement the ability of exitOnTerminationInGUI
            "initializeConnectionsOnStartup": False, # TODO: implement the ability of initializeConnectionsOnStartup
            "refreshRate": 1, # TODO: implement the ability of refreshRate
            "generateNAckMessages": False, # TODO: implement the ability of generateNAckMessages
            "handleEmptyEventQueue": True, # TODO: implement the ability of handleEmptyEventQueue

            # Seed for random numbers
            "useSameSeedAsInPreviousRun": False, # TODO: implement the ability of useSameSeedAsInPreviousRun
            "useFixedSeed": False, # TODO: implement the ability of useFixedSeed
            "fixedSeed": 77654767, # TODO: implement the ability of fixedSeed

            # Logging
            "logFileName": "logfile.txt", # TODO: implement the ability of logFileName
            "outputToConsole": True, # TODO: implement the ability of outputToConsole
            "logToTimeDirectory": True, # TODO: implement the ability of logToTimeDirectory
            "logConfiguration": True, # TODO: implement the ability of logConfiguration
            "eagerFlush": False, # TODO: implement the ability of eagerFlush

            # GUI
            "extendedControl": True, # TODO: implement the ability of extendedControl
            "drawArrows": False, # TODO: implement the ability of drawArrows
            "drawRulers": True, # TODO: implement the ability of drawRulers
            "zoomStep": 1.2, # TODO: implement the ability of zoomStep
            "wheelZoomStep": 1.05, # TODO: implement the ability of wheelZoomStep
            "minZoomFactor": 0.05, # TODO: implement the ability of minZoomFactor
            "draw3DGraphNodesInProperOrder": True, # TODO: implement the ability of draw3DGraphNodesInProperOrder
            "usePerspectiveView": True, # TODO: implement the ability of usePerspectiveView
            "perspectiveViewDistance": 40, # TODO: implement the ability of perspectiveViewDistance

            # Background MAP
            "useMap": False, # TODO: implement the ability of useMap
            "map": "Map.mp", # TODO: implement the ability of map

            # Default Models
            "DefaultMessageTransmissionModel": "ConstantTime", # TODO: implement the ability of DefaultMessageTransmissionModel
            "DefaultConnectivityModel": "UDG", # TODO: implement the ability of DefaultConnectivityModel
            "DefaultDistributionModel": "Random", # TODO: implement the ability of DefaultDistributionModel
            "DefaultInterferenceModel": "NoInterference", # TODO: implement the ability of DefaultInterferenceModel
            "DefaultMobilityModel": "NoMobility", # TODO: implement the ability of DefaultMobilityModel
            "DefaultReliabilityModel": "ReliableDelivery", # TODO: implement the ability of DefaultReliabilityModel
            "showModelsOfAllProjects": False, # TODO: implement the ability of showModelsOfAllProjects

            # Node Collection and Transformation
            "guiPositionTransformation2D": "sinalgo.gui.transformation.Transformation2D", # TODO: implement the ability of guiPositionTransformation2D
            "guiPositionTransformation3D": "sinalgo.gui.transformation.Transformation3D", # TODO: implement the ability of guiPositionTransformation3D
            "nodeCollection2D": "sinalgo.runtime.nodeCollection.Geometric2DNodeCollection", # TODO: implement the ability of nodeCollection2D
            "nodeCollection3D": "sinalgo.runtime.nodeCollection.Geometric3DNodeCollection", # TODO: implement the ability of nodeCollection3D

            # Export Settings
            "epsToPdfCommand": "epstopdf %s", # TODO: implement the ability of epsToPdfCommand
            "epsDrawDeploymentAreaBoundingBox": True, # TODO: implement the ability of epsDrawDeploymentAreaBoundingBox
            "epsDrawBackgroundWhite": True, # TODO: implement the ability of epsDrawBackgroundWhite

            # Animation Settings
            "showMessageAnimations": False, # TODO: implement the ability of showMessageAnimations
            "messageAnimationEnvelopeWidth": 30, # TODO: implement the ability of messageAnimationEnvelopeWidth
            "messageAnimationEnvelopeHeight": 20, # TODO: implement the ability of messageAnimationEnvelopeHeight

            # Diverse Settings
            "showOptimizationHints": True, # TODO: implement the ability of showOptimizationHints
            "drawEdges": True, # TODO: implement the ability of drawEdges
            "drawNodes": True, # TODO: implement the ability of drawNodes
            "shownEventQueueSize": 10, # TODO: implement the ability of shownEventQueueSize
            "outputTextFieldHeight": 200, # TODO: implement the ability of outputTextFieldHeight
            "arrowLength": 8, # TODO: implement the ability of arrowLength
            "arrowWidth": 2, # TODO: implement the ability of arrowWidth
            "defaultRoundNumber": 1 # TODO: implement the ability of defaultRoundNumber
        }
        self.config = {}

    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print(f"Config file '{self.config_file}' not found.")
            self.config = self.default_config  # Load default config if file not found
        except json.JSONDecodeError:
            print(f"Error decoding JSON from '{self.config_file}'.")
            self.config = self.default_config  # Load default config on JSON decode error

        # Merge default config with loaded config to ensure all keys are populated
        self.config = self._merge_configs(self.default_config, self.config)

    def _merge_configs(self, default_config, loaded_config):
        merged_config = default_config.copy()
        for key, value in loaded_config.items():
            if isinstance(value, dict) and key in default_config:
                merged_config[key] = self._merge_configs(default_config[key], value)
            else:
                merged_config[key] = value
        return merged_config

    def get_value(self, key):
        keys = key.split('.')
        current = self.config
        for k in keys:
            current = current.get(k)
            if current is None:
                return None
        return current
    
    def export_config(self, output_file):
        with open(output_file, 'w') as f:
            json.dump(self.config, f, indent=4)

# # Usage example
# config = AppConfig('config.json')
# config.load_config()
# config.export_config("exported_config.json")

# # Accessing values
# dimensions = config.get_value('dimensions')
# dimX = config.get_value('dimX')
# dimY = config.get_value('dimY')
# dimZ = config.get_value('dimZ')

# print(f"Dimensions: {dimensions}")
# print(f"dimX: {dimX}")
# print(f"dimY: {dimY}")
# print(f"dimZ: {dimZ}")
