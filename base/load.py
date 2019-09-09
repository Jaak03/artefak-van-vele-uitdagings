from features.moment import Moment;

class LoadFeatures:
    def __init__( self, cout, env, req ):
        cout.state( 'Compiling features for ' + req + ' images.' );
        self.cout = cout;
        self.env = env;
        self.req = req;

        cout.state( 'Loading feature classes.' );

        # Calling feature classes.
        self.setMoments();
    
    def setMoments( self ):
        self.cout.comment( 'Setting moments.' );
        moment = Moment( self.cout, self.env, self.req );