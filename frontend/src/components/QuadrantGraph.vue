<script setup>
import { ref } from "vue";
import { VueUiQuadrant } from "vue-data-ui";

const config = ref({
        responsive: false,
        theme: '',
        customPalette: [],
        useCssAnimation: true,
        zoomAnimationFrames: 20,
        downsample: {
            threshold: 500
        },
        style: {
            fontFamily: 'inherit',
            chart: {
                height: 512,
                width: 512,
                backgroundColor: '#000000ff',
                color: '#ffffffff',
                layout: {
                    labels: {
                        quadrantLabels: {
                            show: true,
                            tl: {
                                text: 'Top left',
                                color: '#1A1A1Aff',
                                fontSize: 16,
                                bold: true
                            },
                            tr: {
                                text: 'Top right',
                                color: '#1A1A1Aff',
                                fontSize: 16,
                                bold: true
                            },
                            br: {
                                text: 'Bottom right',
                                color: '#1A1A1Aff',
                                fontSize: 16,
                                bold: true
                            },
                            bl: {
                                text: 'Bottom left',
                                color: '#1A1A1Aff',
                                fontSize: 16,
                                bold: true
                            }
                        },
                        plotLabels: {
                            showAsTag: false,
                            show: true,
                            fontSize: 10,
                            color: '#1A1A1Aff',
                            offsetY: 8,
                            rounding: 0,
                            x: {
                                formatter: null
                            },
                            y: {
                                formatter: null
                            }
                        },
                        axisLabels: {
                            show: true,
                            fontSize: 14,
                            color: {
                                positive: '#0000FF',
                                negative: '#FF0000'
                            }
                        }
                    },
                    grid: {
                        stroke: '#e1e5e8ff',
                        strokeWidth: 1.5,
                        showArrows: true,
                        graduations: {
                            stroke: '#e1e5e8ff',
                            strokeWidth: 0.5,
                            show: true,
                            steps: 5,
                            fill: true,
                            color: '#e1e5e8ff',
                            roundingForce: 10
                        },
                        xAxis: {
                            min: -100,
                            max: 100,
                            auto: true,
                            name: 'x Axis'
                        },
                        yAxis: {
                            min: -100,
                            max: 100,
                            auto: true,
                            name: 'y Axis'
                        }
                    },
                    plots: {
                        radius: 6,
                        outline: true,
                        outlineColor: 'rgba(255, 255, 255, 1)',
                        outlineWidth: 1
                    },
                    areas: {
                        show: true,
                        opacity: 40,
                        useGradient: true
                    }
                },
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
                        text: '',
                        fontSize: 16,
                        bold: false
                    }
                },
                tooltip: {
                    show: true,
                    color: '#ffffffff',
                    backgroundColor: '#000000ff',
                    fontSize: 14,
                    customFormat: null,
                    borderRadius: 4,
                    borderColor: '#e1e5e8',
                    borderWidth: 1,
                    backgroundOpacity: 30,
                    position: 'center',
                    offsetY: 24,
                    roundingValue: 0,
                    showShape: true
                },
                legend: {
                    show: true,
                    bold: true,
                    backgroundColor: '#000000ff',
                    color: '#ffffffff',
                    fontSize: 14
                }
            }
        },
        table: {
            show: false,
            responsiveBreakpoint: 400,
            th: {
                backgroundColor: '#000000ff',
                color: '#ffffffff',
                outline: 'none'
            },
            td: {
                backgroundColor: '#000000ff',
                color: '#ffffffff',
                outline: 'none',
                roundingValue: 0
            }
        },
        userOptions: {
            show: true,
            showOnChartHover: false,
            keepStateOnChartLeave: true,
            position: 'right',
            buttons: {
                tooltip: true,
                pdf: true,
                csv: true,
                img: true,
                table: true,
                labels: true,
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
                tooltip: 'Toggle tooltip',
                pdf: 'Download PDF',
                csv: 'Download CSV',
                img: 'Download PNG',
                table: 'Toggle table',
                labels: 'Toggle labels',
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
        translations: {
            category: 'Category',
            item: 'Item',
            side: 'Side'
        }
    });

const dataset = ref([
    {
        name: 'Group 1',
        shape: 'circle',
        color: '#42d392',
        series: [
            {
                name: 'Item 1',
                x: 5,
                y: 5
            },
            {
                name: 'Item 2',
                x: -3,
                y: -3
            }
        ]
    },
    {
        name: 'Group 2',
        shape: 'star',
        color: '#6376DD',
        series: [
            {
                name: 'Item 1',
                x: 2,
                y: -6
            },
            {
                name: 'Item 2',
                x: -2,
                y: 7
            }
        ]
    }
]);

</script>
<template>
    <!-- Using a wrapper is optional -->
    <div :style="{ width: '600px'}">
        <VueUiQuadrant
            :config="config"
            :dataset="dataset"
        />
    </div>
</template>