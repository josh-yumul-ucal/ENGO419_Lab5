function handle = drawEllipse(col, a, b, x0, y0, phi);

%   drawEllipse draws an ellipse with characteristics given by the user.
%   The function returns 'handle', which can then be used to further 
%   customize the ellipse. 
%
%   Written by: Victoria Hoyle, December 2003
%   For ENGO 419/Fall 2023
%   Copyright (c) 2003
%
%   Input parameters:
%       col         matlab color string, ie: 'r', 'g', 'b', etc.
%       a           Semi-major axis
%       b           Semi-minor axis
%       x0          X coordinate of the ellipse centre
%       y0          Y coordinate of the ellipse centre
%       phi         Angle between x-axis and the major axis IN DEGREES
%
%   Output:
%       handle      Handle of the plotted object
%
%   Examples of use:
%   drawEllipse(2, 4);  - semi-major and semi-minor axes with no rotation or translation
%   drawEllipse(2, 4, 90);  - semi-major, semi-minor and rotation as input and no translation
%   drawEllipse(2, 4, 10, 10);  - semi-major, semi-minor, x0 and y0 as input and no rotation
%   drawEllipse(2, 4, 10, 10, 90);  - semi-major, semi-minor, x0, y0 and rotation as input
%   
%   %% To draw more than more ellipse on the same plot:
%   figure;
%   hold on;
%   drawEllipse(2, 4);          % draw the first ellipse on the figure
%   drawEllipse(2, 4, 10, 10);  % draw a second ellipse on the figure
%   hold off;
%   %% You should now have a figure with two ellipses on it, which you can
%   scale to the dimensions of your network by clicking on the Figure menu
%   bar: "Tools", and toggle Edit Plot on.  Then double click on the axes 
%   and turn off Auto limits.   

if (nargin < 2)|(nargin > 6)
    error('Too few or too many input arguments; please see function comments for help.');
    
elseif(nargin == 3) % The ellipse is centred at (0,0) and the major axis does not have a rotation with respect to the x-axis.
    x0 = 0;
    y0 = 0;
    phi = 0;
    
elseif(nargin == 4) % The ellipse is centred at (0,0) but the major axis has a rotation with respect to the x-axis
    phi = x0;
    x0 = 0;
    y0 = 0;
    
elseif(nargin == 5) % The major axis does not have a rotation with respect to the x-axis.  
    phi = 0;
    
end

% convert phi to radians for computations
phi = phi* pi / 180;

theta = [-0.01:0.01:2*pi];

% create x and y coordinates for an untransformed ellipse with axes a and b 
x = a*cos(theta);
y = b*sin(theta);

% transform the ellipse according to shift and rotation parameters given
X = cos(phi)*x - sin(phi)*y;
Y = sin(phi)*x + cos(phi)*y;
X = X + x0;
Y = Y + y0;

% plot the ellipse and return the handle to the figure generated
handle = plot(X,Y,col, 'linewidth', 2);

% Reference: 
% Lei Wang, 2003