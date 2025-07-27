<script setup>
import { ref } from "vue";
import { VueUiCirclePack } from "vue-data-ui";

const config = ref({
        theme: '',
        customPalette: [],
        userOptions: {
            show: true,
            showOnChartHover: false,
            keepStateOnChartLeave: true,
            position: 'right',
            buttons: {
                tooltip: false,
                pdf: true,
                csv: true,
                img: true,
                table: true,
                labels: false,
                fullscreen: true,
                sort: false,
                stack: false,
                animation: false,
                annotator: true
            },
            callbacks: {
                animation: null,
                annotator: null,
                csv: null,
                fullscreen: null,
                img: null,
                labels: null,
                pdf: null,
                sort: null,
                stack: null,
                table: null,
                tooltip: null
            },
            buttonTitles: {
                open: 'Open options',
                close: 'Close options',
                pdf: 'Download PDF',
                csv: 'Download CSV',
                img: 'Download PNG',
                table: 'Toggle table',
                fullscreen: 'Toggle fullscreen',
                annotator: 'Toggle annotator'
            },
            print: {
                allowTaint: false,
                backgroundColor: '#FFFFFFff',
                useCORS: false,
                onclone: null,
                scale: 2,
                logging: false
            }
        },
        table: {
            show: false,
            responsiveBreakpoint: 400,
            th: {
                backgroundColor: '#FFFFFFff',
                color: '#1A1A1Aff',
                outline: 'none'
            },
            td: {
                backgroundColor: '#FFFFFFff',
                color: '#1A1A1Aff',
                outline: 'none'
            },
            columnNames: {
                datapoint: 'Datapoint',
                value: 'Value'
            }
        },
        style: {
            fontFamily: 'inherit',
            chart: {
                backgroundColor: '#000000ff',
                color: '#ffffffff',
                title: {
                    text: 'Title',
                    color: '#1A1A1Aff',
                    fontSize: 20,
                    bold: true,
                    textAlign: 'center',
                    paddingLeft: 0,
                    paddingRight: 0,
                    subtitle: {
                        color: '#A1A1A1ff',
                        text: 'Subtitle',
                        fontSize: 16,
                        bold: false
                    }
                },
                circles: {
                    stroke: '#FFFFFFff',
                    strokeWidth: 1,
                    gradient: {
                        show: true,
                        intensity: 40
                    },
                    labels: {
                        name: {
                            fontSizeRatio: 1,
                            show: true,
                            bold: false,
                            offsetY: 0,
                            color: 'auto'
                        },
                        value: {
                            fontSizeRatio: 1,
                            show: true,
                            color: 'auto',
                            rounding: 0,
                            prefix: '',
                            suffix: '',
                            formatter: null,
                            bold: false,
                            offsetY: 0
                        }
                    },
                    zoom: {
                        show: true,
                        shadowForce: 1,
                        opacity: 0.8,
                        animationFrameMs: 200,
                        zoomRatio: 1,
                        label: {
                            name: {
                                fontSize: 14,
                                bold: false,
                                offsetY: 0,
                                color: 'auto'
                            },
                            value: {
                                fontSize: 14,
                                bold: false,
                                offsetY: 0,
                                rounding: 0,
                                prefix: '',
                                suffix: '',
                                formatter: null,
                                color: 'auto'
                            }
                        }
                    }
                }
            }
        }
    });

const dataset = ref([
    {
        name: 'Datapoint A',
        value: 100.123,
        color: null
    },
    {
        name: 'Datapoint B',
        value: 90.234,
        color: null
    },
    {
        name: 'Datapoint C',
        value: 80.345,
        color: null
    },
    {
        name: 'Datapoint D',
        value: 70.456,
        color: null
    },
    {
        name: 'Datapoint E',
        value: 60.789,
        color: null
    },
    {
        name: 'Datapoint F',
        value: 50.891,
        color: null
    },
    {
        name: 'Datapoint G',
        value: 40.912,
        color: null
    },
    {
        name: 'Datapoint H',
        value: 30.123,
        color: null
    },
    {
        name: 'Datapoint I',
        value: 20.234,
        color: null
    },
    {
        name: 'Datapoint J',
        value: 10.345,
        color: null
    }
]);

</script>
<template>
    <!-- Using a wrapper is optional -->
    <div :style="{ width: '600px'}">
        <VueUiCirclePack
            :config="config"
            :dataset="dataset"
        />
    </div>
</template>