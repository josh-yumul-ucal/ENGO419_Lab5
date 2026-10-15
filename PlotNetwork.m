function handle = PlotNetwork(Xo,pars, el1, el2,ObsDist)
%input station coordinate file of parameters Xo
%                                 station ellipse matrix el1
%                                 relative ellipse matrix el2
%                                 distance observations ObsDist
%
% Use the function DrawEllipse to output the ellipses
%
% You will need to scale the ellipse factors to be visible at this scale
% (suggest 2000-4000 x)
%
set(figure, 'Name', 'Network Plot');

for i			= 1:pars/2
    x_adj(i) 	= Xo(i,2);  % X network coordinates
    y_adj(i) 	= Xo(i,3);  % Y network coordinates
    
end

scale           = 4000;
scatter(x_adj, y_adj, 5);
axis equal;
%labels          = ['1';'2';'3';'4';'5';'6';'7';'8'];
labels          = ['1';'2';'3';'4';'5';'6';'7'];

hold on;

% Dispaying the numbers of the points of the network
for i			= 1:pars/2
    text(x_adj(i)+20, y_adj(i)-25, labels(i,:));  
end

% Putting lines to connect the points you have measurements for
for i           = 1:length(ObsDist)
    line([x_adj(ObsDist(i,1)) x_adj(ObsDist(i,2))], [y_adj(ObsDist(i,1)) y_adj(ObsDist(i,2))]);
end

hold on;
title('Fig : Network Plot');
xlabel( 'X (m)');
ylabel( 'Y (m)');

grid on;

%% plot error ellipses here...