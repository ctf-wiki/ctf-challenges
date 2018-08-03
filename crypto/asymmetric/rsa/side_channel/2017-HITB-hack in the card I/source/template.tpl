<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <title>wave</title>
    <style>
        * {
            border: 0;
            margin: 0;
            padding: 0;
        }

        html, body {
            width: 100%;
            height: 100%;
            font-family: Helvetica Neue,Helvetica,PingFang SC,Hiragino Sans GB,Microsoft YaHei,SimSun,sans-serif;
        }

        #chart {
            width: 1000px;
            height: 500px;
            position: relative;
        }

        input {
            border: 1px solid #000;
        }

        .query {
            padding: 20px 40px;
        }

        .footer {
            position: relative;
        }

        .toolbar {
            display: inline-block;
            border: 1px solid #eee;
            border-radius: 3px;
            margin-left: 100px;
        }

        .info {
            display: inline-block;
            color: #888;
            height: 186px;
            position: absolute;
            top: 0;
            padding: 10px 40px;
        }

        .toolbar button {
            color: #fff;
            background-color: #20a0ff;
            display: inline-block;
            line-height: 1;
            white-space: nowrap;
            cursor: pointer;
            border: 1px solid #20a0ff;
            text-align: center;
            box-sizing: border-box;
            outline: none;
            margin: 0 0 0 10px;
            padding: 10px 15px;
            font-size: 14px;
            border-radius: 4px;
        }

        .toolbar button:hover {
            background: #4db3ff;
            border-color: #4db3ff;
            color: #fff;
        }

        .toolbar .input-group {
            width: 120px;
            position: relative;
            display: inline-block;
        }

        .toolbar .input-unit {
            width: 40px;
            height: 100%;
            display: inline-block;
            position: absolute;
            right: 0;
            top: 0;
            line-height: 36px;
            text-align: center;
            color: #999;
        }

        .toolbar input {
            width: 100%;
            appearance: none;
            background-color: #fff;
            background-image: none;
            border-radius: 4px;
            border: 1px solid #bfcbd9;
            box-sizing: border-box;
            color: #1f2d3d;
            display: inline-block;
            font-size: inherit;
            height: 36px;
            line-height: 1;
            outline: none;
            padding: 3px 40px 3px 10px;
            transition: border-color .2s cubic-bezier(.645,.045,.355,1);
        }

        .toolbar label {
            text-align: right;
            vertical-align: middle;
            float: left;
            font-size: 14px;
            color: #48576a;
            line-height: 1;
            padding: 11px 12px 11px 0;
            box-sizing: border-box;
        }

        .toolbar .row {
            margin: 10px 0;
        }

        .toolbar #result {
            display: inline-block;
            height: 30px;
            line-height: 30px;
            padding: 3px 10px;
        }

        .toolbar h3 {
            font-weight: 400;
            color: #1f2f3d;
            font-size: 22px;
            margin: 10px 0;
        }
         
        #loading {
            position: absolute;
            top: 50%;
            width: 100%;
            text-align: center;
            font-size: 20px;
        }
    </style>
</head>

<body>
    <div class="chart" id="chart">
        <div id="loading">loading...</div>
    </div>
    <div class="footer">
        <div class="toolbar">
            <div class="query">
                <h3>数据查询</h3>
                <div class="row">
                    <label>时间（X轴）</label>
                    <div class="input-group">
                        <input type="text" id="value"><span class="input-unit">ms</span>
                    </div><button id="query">查询</button>
                </div>
                <div class="row"><p><label>电压（Y轴）</label><span id="result">0</span> mV</p></div>
            </div>
        </div>
        <p class="info">滚动鼠标滚轮缩放图表，按住鼠标可以左右拖动图表</p>
    </div>
    <script>
        var data ={{#data}};
    </script>
    <script src="./build.js"></script>
    <script>
        document.getElementById( 'loading' ).style.display = 'none';
    </script>
</body>

</html>
