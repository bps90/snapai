import json
import yaml

class Configuration:
    
    def __init__(self, network_size=100, node_count=50, transmission_range=10.0, simulation_time=1000):
        
        
        """
        ================================================================================
        Simulation Area
        ================================================================================
        """
        self.dimenssions = 3 #allow to be 3
        self.dimX = 500
        self.dimY = 500
        self.dimZ = 500

        """
        ================================================================================
        Simulation
        ================================================================================
        """

        """
        Switches between synchronous and asynchronous mode. 
        TODO: to implement this mode
        """
        self.asynchronousMode = False 

        """
        If set to true, the runtime acquires a new position for each node from the mobility model at the start of each round.
        Enable this flag if the selected mobility model for any node may alter its position.
        Set this flag to FALSE for static graphs where nodes do not change position to improve performance.
        TODO: to implement this mobility
        """
        self.mobility = True  # or False

        """
        If set to true, the chosen interference model is called at the
        end of every round to test for interfering packets.
        To increase performance, set this flag to FALSE if you do not
        consider interference.
        TODO: to implement this interference
        """
        self.interference = True

        """
        Set this flag to true if interference only decreases if
        fewer messages are being sent and increases if more messages
        are being sent.
        If this flag is NOT set, interference for all messages currently
        being sent is reevaluated whenever a new message is being sent, and
        whenever a message stops being sent. When this flag is set,
        interference tests are reduced to a minimum, using the additivity
        property.
        This flag only affects the asynchronous mode. In synchronous mode,
        interference is checked exactly once for every message in every round.
        TODO: to implement this additive interference
        """
        self.interferenceIsAdditive = True

        """
        Set this flag to true if a node can receive messages while
        it is sending messages itself, otherwise to false. This flag
        is only relevant if interference is turned on, and it must be
        handled properly in the used interference model.
        TODO: to implement ability of canReceiveWhileSending
        """
        self.canReceiveWhileSending = True

        """
        Set this flag to true if a node can receive multiple messages
        in parallel, otherwise to false. When set to false, concurrent
        packets are all dropped. This flag is only relevant if
        interference is turned on, and it must be handled properly in
        the used interference model.
        TODO: to implement ability of canReceiveMultiplePacketsInParallel
        """
        self.canReceiveMultiplePacketsInParallel = True

        """
        The type of the edge to be created in the edge factory.
        This field is private, but has a setter and getter method.
        TODO: I do not know if it is necessary
        """
        self.edge_type = "Edge"

        """
        If set to true, the application exits as soon as the
        termination criteria is met. This flag only affects
        the GUI mode.
        TODO: to implement ability of exitOnTerminationInGUI
        """
        self.exitOnTerminationInGUI = False

        """
        If set true, in asynchronous mode the connections are initialized
        before the first event executes. Note that this flag is useless in synchronous mode
        as the connections are updated in every step anyway.
        TODO: to implement ability of initializeConnectionsOnStartup
        """
        self.initializeConnectionsOnStartup = False

        """
        Defines how often the GUI is updated. The GUI is
        redrawn after every refreshRate-th round.
        TODO: to implement ability of refreshRate
        """
        self.refreshRate = 1

        """
        If set to true, the framework will inform a sender whenever 
        a unicast message is dropped. In synchronous mode, the sender 
        is informed in the round after the message should have arrived, and 
        immediately upon arrival in asynchronous mode.
        TODO: to implement ability of generateNAckMessages
        """
        self.generateNAckMessages = False

        """
        This flag only affects the asynchronous simulation mode. 
        When set to true, the framework calls handleEmptyEventQueue 
        on the project specific CustomGlobal whenever the event queue 
        becomes empty.
        TODO: to implement ability of handleEmptyEventQueue
        """
        self.handleEmptyEventQueue = True

        """
        ================================================================================
        Seed for random numbers
        ================================================================================
        """

        """
        If set to true, the random number generators of the framework use the same seed as in the previous run.
        TODO: to implement ability of useSameSeedAsInPreviousRun
        """
        self.useSameSeedAsInPreviousRun = False

        """
        If set to true, and useSameSeedAsInPreviousRun is set to false, 
        the random number generators of the framework uses the specified fixed seed.
        TODO: to implement ability of useFixedSeed
        """
        self.useFixedSeed = False

        """
        The seed to be used by the random number generators
        if useFixedSeed is set to true.
        TODO: to implement ability of fixedSeed
        """
        self.fixedSeed = 77654767

        """
        ================================================================================
        Logging
        ================================================================================
        TODO: to implement the python logging style 
        """


        """
        Name of the default log file, used by the system,
        but also for use by the end-user. (This log file
        is stored under sinalgo.runtime.Global.log.)
        TODO: to implement ability of logFileName
        """
        self.logFileName = "logfile.txt"

        """
        Redirects the default log file to the console.
        No logfile will be created if set to true.
        TODO: to implement ability of outputToConsole
        """
        self.outputToConsole = True

        """
        Indicates whether all log-files of the current simulation 
        are stored in a new directory. The name of the new directory
        is given by the string-representation of the date
        when the simulation starts.
        TODO: to implement ability of logToTimeDirectory
        """
        self.logToTimeDirectory = True

        """
        If set to true, the system configuration is written to
        the default log file after the application has been started.
        TODO: to implement ability of logConfiguration
        """
        self.logConfiguration = True

        """
        If set to true, the log files are flushed every time
        a new log is added.
        TODO: to implement ability of eagerFlush
        """
        self.eagerFlush = False

        """
        ================================================================================
        GUI
        ================================================================================
        TODO: maybe remove all
        """
        
        """
        If true, the application shows an extended control panel.
        TODO: to implement ability of extendedControl
        """
        self.extendedControl = True

        """
        If true, the graph edges are drawn as directed arrows,
        otherwise simple lines.
        TODO: to implement ability of drawArrows
        """
        self.drawArrows = False

        """
        If true, draw ruler along the axes of the graph
        TODO: to implement ability of drawRulers
        """
        self.drawRulers = True

        """
        Fraction of the old and new zoom values for a zoom step.
        TODO: to implement ability of zoomStep
        """
        self.zoomStep = 1.2

        """
        Fraction of the old and new zoom values for a zoom 
        step when zooming with the mouse wheel.
        TODO: to implement ability of wheelZoomStep
        """
        self.wheelZoomStep = 1.05

        """
        The minimum required zoom
        TODO: to implement ability of minZoomFactor
        """
        self.minZoomFactor = 0.05

        """
        If set to true, the nodes are ordered according to their 
        elevation before drawing, such that nodes closer to the 
        viewer are drawn on top. This setting only applies to 3D.
        TODO: to implement ability of draw3DGraphNodesInProperOrder
        """
        self.draw3DGraphNodesInProperOrder = True

        """
        If set to true and in 3D mode, the cube is drawn
        with perspective.
        TODO: to implement ability of usePerspectiveView
        """
        self.usePerspectiveView = True

        """
        Factor that defines the distance of the observer from the cube
        when using the perspective view in 3D. Default: 40
        TODO: to implement ability of perspectiveViewDistance
        """
        self.perspectiveViewDistance = 40

        """
        ================================================================================
        Background MAP
        ================================================================================
        TODO: maybe remove all
        """

        """
        If set to true, the background of a 2D simulation is colored
        according to a map, specified in a map-file, specified
        by the field map
        TODO: to implement ability of useMap
        """
        self.useMap = False

        """
        In 2D, the background can be colored depending on a map file.
        This field contains the file name for this map, which is supposed
        to be located in the source folder of the current project.
        The map is only painted if useMap is set to true.
        TODO: to implement ability of map
        """
        self.map = "Map.mp"


        """
        ================================================================================
        The models that are selected by default.
        ================================================================================
        """

        # The message transmission model used when none is specified
        self.DefaultMessageTransmissionModel = "ConstantTime"

        # Default connectivity model used when none is specified
        self.DefaultConnectivityModel = "UDG"

        # Default distribution model used when none is specified
        self.DefaultDistributionModel = "Random"

        # Default interference model used when none is specified
        self.DefaultInterferenceModel = "NoInterference"

        # Default mobility model used when none is specified
        self.DefaultMobilityModel = "NoMobility"

        # Default reliability model used when none is specified
        self.DefaultReliabilityModel = "ReliableDelivery"

        # Default node implementation used when none is specified
        DefaultNodeImplementation = "DummyNode"

        # Show the models implemented by all projects in the drop
        # down options. When set to false, only the models by the
        # selected project and the default project are shown.
        self.showModelsOfAllProjects = False

        """
        ================================================================================
        The default transformation and node collection implementations for the 2D / 3D case                                                                       =
        ================================================================================
        TODO: maybe remove all
        """

                
        """
        Node storage, position transformation
        Transformation implementation for 2D. (This is
        used to translate between the logic positions used by
        the simulation to the 2D coordinate system used by the
        GUI to display the graph)
        """
        self.guiPositionTransformation2D = "sinalgo.gui.transformation.Transformation2D"

        """
        Transformation implementation for 3D. (This is
        used to translate between the logic positions used by
        the simulation to the 2D coordinate system used by the
        GUI to display the graph)
        """
        self.guiPositionTransformation3D = "sinalgo.gui.transformation.Transformation3D"

        """
        Node collection implementation for 2D.
        """
        self.nodeCollection2D = "sinalgo.runtime.nodeCollection.Geometric2DNodeCollection"

        """
        Node collection implementation for 3D.
        """
        self.nodeCollection3D = "sinalgo.runtime.nodeCollection.Geometric3DNodeCollection"
        
        """
        ================================================================================
        Export Settings
        ================================================================================
        TODO: maybe remove all
        """

        self.epsToPdfCommand = "epstopdf %s"

        """
        EPS 2 PDF command:
        This is the command that is used to convert an EPS file 
        into a PDF file. You can use the following parameters:
        %s is the complete path from the root folder of the
            framework to the SOURCE file (the eps)
        %t is the complete path from the root folder of the
            framework to the TARGET file (the pdf)
        These placeholders are set by the framework.
        Example:
        'epstopdf %s'
        """

        self.epsDrawDeploymentAreaBoundingBox = True

        """
        Enables the drawing of the bounding box of the deployment to EPS/PDF.
        """

        self.epsDrawBackgroundWhite = True

        """
        Indicates whether the background in the ps should be
        white or gray.
        The gray version is easier to understand (especially in 3D)
        but the white one should be more useful to be imported in reports.
        """

       
        """
        ================================================================================
        Animation Settings
        ================================================================================
        """

        """
        Draw an envelope for each message that is being sent
        """
        self.showMessageAnimations = False


        """
        Width of the envelope (when the message animation is enabled)
        """
        self.messageAnimationEnvelopeWidth = 30


        """
        Height of the envelope (when the message animation is enabled)
        """
        self.messageAnimationEnvelopeHeight = 20


        """
        Color of the envelope (when the message animation is enabled)
        """
        #messageAnimationEnvelopeColor = Color.YELLOW



        """
        ================================================================================
        Diverse Settings
        ================================================================================
        """

        """
        Show hints on how to further optimize the simulation when
        some parameters seem not to be set optimally.
        """
        self.showOptimizationHints = True

        """
        Indicates whether the edges are drawn in the default
        draw implementation for the graph.
        """
        self.drawEdges = True

        """
        Indicates whether the nodes are drawn in the default
        draw implementation for the graph.
        """
        self.drawNodes = True

        
        """
        The number of future events that are shown in the control
        panel
        """
        self.shownEventQueueSize = 10

        
        """
        Height of the output text field in pixels.
        """
        self.outputTextFieldHeight = 200

        
        """
        The length of the arrows. This length is multiplied by the current zoomLevel.
        """
        self.arrowLength = 8

        
        """
        The width of the arrows. This width is multiplied by the current zoomLevel.
        """
        self.arrowWidth = 2

        """
        The default value of the rounds field.
        """
        self.defaultRoundNumber = 1



        self.network_size = network_size
        self.node_count = node_count
        self.transmission_range = transmission_range
        self.simulation_time = simulation_time

    def to_dict(self):
        return {
            'network_size': self.network_size,
            'node_count': self.node_count,
            'transmission_range': self.transmission_range,
            'simulation_time': self.simulation_time
        }

    def from_dict(self, config_dict):
        self.network_size = config_dict.get('network_size', self.network_size)
        self.node_count = config_dict.get('node_count', self.node_count)
        self.transmission_range = config_dict.get('transmission_range', self.transmission_range)
        self.simulation_time = config_dict.get('simulation_time', self.simulation_time)

    def save_to_json(self, file_path):
        with open(file_path, 'w') as file:
            json.dump(self.to_dict(), file, indent=4)

    def load_from_json(self, file_path):
        with open(file_path, 'r') as file:
            config_dict = json.load(file)
            self.from_dict(config_dict)

    def save_to_yaml(self, file_path):
        with open(file_path, 'w') as file:
            yaml.dump(self.to_dict(), file, default_flow_style=False)

    def load_from_yaml(self, file_path):
        with open(file_path, 'r') as file:
            config_dict = yaml.safe_load(file)
            self.from_dict(config_dict)

# Example usage
"""config = Configuration()
config.save_to_json('config.json')
config.save_to_yaml('config.yaml')

config_loaded = Configuration()
config_loaded.load_from_json('config.json')
print(config_loaded.to_dict())

config_loaded.load_from_yaml('config.yaml')
print(config_loaded.to_dict())
"""