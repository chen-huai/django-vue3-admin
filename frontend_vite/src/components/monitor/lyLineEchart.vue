<template>
    <div ref="lyechartmain"  style="width: 100%;height: 280px"></div>
</template>

<script setup>
    import {onBeforeUnmount, onMounted, reactive, watch,ref,nextTick} from "vue";
    // 按需引入echarts
    import echarts from "@/components/analysis/echartsInstall";

    const props = defineProps(['modelValue'])
    const emit = defineEmits(['update:modelValue'])

    const state = reactive({
        contentValue: null,
        timeout: null,
        echartData: {
            uData: [],
            dData: [],
            aData: []
        }

    })

    let myChart = ref(null)
    let option = reactive({})
    let lyechartmain = ref(null)
    onMounted(() => {//需要获取到element,所以是onMounted的Hook
        setTimeout(() => {
            nextTick(()=>{
                myChart.value = echarts.init(lyechartmain.value);
                state.contentValue = props.modelValue
                addData(state.contentValue.up,state.contentValue.down)
                initEcharts()
            })
        },200)
    });
    onBeforeUnmount(() => {
        window.onresize = null;
    })
    // 侦听文本变化并传给外界
    watch(() => state.contentValue, (n) => {
        debounce(() => {
            emit('update:modelValue', state.contentValue)
        })
    })
    // 侦听默认值 外界第一次传进来一个 v-model 就赋值给 contentValue
    watch(() => props.modelValue, (n) => {
        if (n && n !== state.contentValue) {
            state.contentValue = n
            addData(n.up,n.down)
            initEcharts()

        }
    })
    function initEcharts() {
        var obj = {};
        obj.dataZoom = [];
        obj.unit =  '单位:KB/s';
        obj.tData = state.echartData.aData;
        obj.formatter = function (config) {
            var _config = config, _tips = '';
            for (var i = 0; i < config.length; i++) {
                if (typeof config[i].data == "undefined") return false
                _tips += '<span style="display: inline-block;width: 10px;height: 10px;margin-rigth:10px;border-radius: 50%;background: ' + config[i].color + ';"></span>  ' + config[i].seriesName + '：' + (parseFloat(config[i].data)).toFixed(2) + ' KB/s' + (config.length - 1 !== i ? '<br />' : '')
            }
            return "时间：" + _config[0].axisValue + "<br />" + _tips;
        }
        obj.list = [];
        obj.list.push({ name: '上行', data: state.echartData.uData, circle: 'circle', itemStyle: { color: '#4c8ff1' }, areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ offset: 0, color: 'rgba(76, 143, 241)' }, { offset: 1, color: 'rgba(76, 143, 241)' }], false) }, lineStyle: { width: 1, color: '#aaa' } } );
        obj.list.push({ name: '下行', data: state.echartData.dData, circle: 'circle', itemStyle: { color: '#1cd798' }, areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ offset: 0, color: 'rgba(28, 215, 152)' }, { offset: 1, color: 'rgba(28, 215, 152)' }], false) }, lineStyle: { width: 1, color: '#aaa' } });
        option = format_option(obj)
        option && myChart.value && myChart.value.setOption(option);
        window.onresize = function () {//自适应大小
            myChart.value.resize();
        };
    }
    function addData(up, down) {
        var limit = 16;
        var d = new Date()
        if (state.echartData.uData.length >= limit) state.echartData.uData.splice(0, 1);
        if (state.echartData.dData.length >= limit) state.echartData.dData.splice(0, 1);
        if (state.echartData.aData.length >= limit) state.echartData.aData.splice(0, 1);

        state.echartData.uData.push(up);
        state.echartData.dData.push(down);
        state.echartData.aData.push(d.getHours() + ':' + d.getMinutes() + ':' + d.getSeconds());
    }
     function format_option(obj, type) {
        if(!obj){
            return
        }
        var option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross'
                },
                formatter: obj.formatter
            },
            grid: {
                  left: '3%',
                  right: '3%',
                  bottom: '3%',
                  containLabel: true
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: obj.tData,
                axisLine: {
                    lineStyle: {
                        color: "#666"
                    }
                }
            },
            yAxis: {
                type: 'value',
                name: obj.unit,
                boundaryGap: [0, '100%'],
                min: 0,
                splitLine: {
                    lineStyle: {
                        color: "#ddd"
                    }
                },
                axisLine: {
                    lineStyle: {
                        color: "#666"
                    }
                }
            },
            dataZoom: [{
                type: 'inside',
                start: 0,
                zoomLock: true
            }, {
                start: 0,
                handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                handleSize: '80%',
                handleStyle: {
                    color: '#fff',
                    shadowBlur: 3,
                    shadowColor: 'rgba(0, 0, 0, 0.6)',
                    shadowOffsetX: 2,
                    shadowOffsetY: 2
                }
            }],
            series: []
        };
        if (obj.legend) option.legend = obj.legend;
        if (obj.dataZoom) option.dataZoom = obj.dataZoom;

        for (var i = 0; i < obj.list.length; i++) {
            var item = obj.list[i];
            var series = {
                name: item.name,
                type: item.type ? item.type : 'line',
                smooth: item.smooth ? item.smooth : true,
                symbol: item.symbol ? item.symbol : 'none',
                showSymbol: item.showSymbol ? item.showSymbol : false,
                sampling: item.sampling ? item.sampling : 'average',
                areaStyle: item.areaStyle ? item.areaStyle : {},
                lineStyle: item.lineStyle ? item.lineStyle : {},
                itemStyle: item.itemStyle ? item.itemStyle : {color: 'rgb(0, 153, 238)'},
                symbolSize: 6,
                symbol: 'circle',
                data: item.data
            }
            option.series.push(series);
        }
        return option;
    }
    function debounce (fn, wait = 400)  {
      // console.log('进到了防抖', wait)
      if (state.timeout != null) {
        clearTimeout(state.timeout)
      }
      state.timeout = setTimeout(fn, wait)
    }
    function handleResize() {
        if(myChart.value != null){
            myChart.value.resize();
        }
    }
    defineExpose ({
        debounce,
        handleResize,
        addData,
        initEcharts,
        format_option
    })
</script>

<style scoped>

</style>