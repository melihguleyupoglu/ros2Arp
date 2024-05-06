const express = require('express');
const roslib = require('roslib');

const app = express();
const port = 3000;

let ros = new roslib.Ros({
    url: 'ws://localhost:9090'  // rosbridge_server'ın çalıştığı adres
});

ros.on('connection', function () {
    console.log('Connected to ROS.');
});

ros.on('error', function (error) {
    console.log('Error connecting to ROS: ', error);
});

let cmdVelTopic = new roslib.Topic({
    ros: ros,
    name: '/turtle1/cmd_vel',
    messageType: 'geometry_msgs/Twist'
});

app.get('/', (req, res) => {
    res.send(`
    <html>
    <style>
    .center-div {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        flex-direction: column;
    }

    button {
        margin: 10px;
        padding: 10px 20px;
        font-size: 20px
    }
    </style>
      <body>
        <div class="center-div">
            <button onclick="move('forward')">Move forward</button>
            <button onclick="move('backward')">Move backwards</button>
        </div>
      <script>
        function move(direction) {
            fetch('/move/' + direction);
        }
      </script>
        </body>
    </html>
  `);
});

app.get('/move/:direction', (req, res) => {
    let linearVelocity = (req.params.direction === 'forward') ? 2.0 : -2.0;
    let twist = new roslib.Message({
        linear: {
            x: linearVelocity,
            y: 0.0,
            z: 0.0
        },
        angular: {
            x: 0.0,
            y: 0.0,
            z: 0.0
        }
    });
    cmdVelTopic.publish(twist);
    res.send('Moving ' + req.params.direction);
});

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
