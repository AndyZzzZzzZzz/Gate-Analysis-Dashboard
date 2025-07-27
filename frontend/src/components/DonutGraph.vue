<script setup>
import { ref } from "vue";
import { VueUiDonut } from "vue-data-ui";

const config = ref({
        type: 'classic',
        responsive: false,
        theme: '',
        customPalette: [],
        useCssAnimation: true,
        serieToggleAnimation: {
            show: true,
            durationMs: 500
        },
        startAnimation: {
            show: true,
            durationMs: 1000,
            staggerMs: 50
        },
        useBlurOnHover: true,
        userOptions: {
            show: false,
            showOnChartHover: false,
            keepStateOnChartLeave: true,
            position: 'right',
            buttons: {
                tooltip: true,
                pdf: false,
                csv: false,
                img: false,
                table: false,
                labels: false,
                fullscreen: false,
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
            total: 'Total',
            average: 'Average'
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
                roundingValue: 0,
                roundingPercentage: 0
            },
            columnNames: {
                series: 'Series',
                value: 'Value',
                percentage: 'Percentage'
            }
        },
        style: {
            fontFamily: 'inherit',
            chart: {
                useGradient: true,
                gradientIntensity: 40,
                backgroundColor: '#000001ff',
                color: '#ffffffff',
                padding: {
                    top: 0,
                    right: 0,
                    bottom: 0,
                    left: 0
                },
                width: 512,
                height: 360,
                layout: {
                    curvedMarkers: true,
                    labels: {
                        dataLabels: {
                            show: true,
                            useLabelSlots: false,
                            hideUnderValue: 3,
                            prefix: '',
                            suffix: ''
                        },
                        value: {
                            rounding: 0,
                            show: true,
                            formatter: null
                        },
                        percentage: {
                            color: '#ffffffff',
                            bold: true,
                            fontSize: 18,
                            rounding: 0,
                            formatter: null
                        },
                        name: {
                            color: '#1A1A1Aff',
                            bold: false,
                            fontSize: 14
                        },
                        hollow: {
                            show: true,
                            total: {
                                show: true,
                                bold: false,
                                fontSize: 18,
                                color: '#ffffffff',
                                text: 'Total',
                                offsetY: 0,
                                value: {
                                    color: '#1A1A1Aff',
                                    fontSize: 18,
                                    bold: true,
                                    suffix: '',
                                    prefix: '',
                                    offsetY: 0,
                                    rounding: 0,
                                    formatter: null
                                }
                            },
                            average: {
                                show: true,
                                bold: false,
                                fontSize: 18,
                                color: '#AAAAAAff',
                                text: 'Average',
                                offsetY: 0,
                                value: {
                                    color: '#1A1A1Aff',
                                    fontSize: 18,
                                    bold: true,
                                    suffix: '',
                                    prefix: '',
                                    offsetY: 0,
                                    rounding: 0,
                                    formatter: null
                                }
                            }
                        }
                    },
                    donut: {
                        strokeWidth: 64,
                        borderWidth: 1,
                        useShadow: false,
                        shadowColor: '#1A1A1A',
                        emptyFill: 'rgba(255, 255, 255, 1)'
                    }
                },
                comments: {
                    show: true,
                    showInTooltip: true,
                    width: 100,
                    offsetY: 0,
                    offsetX: 0
                },
                legend: {
                    show: true,
                    bold: false,
                    backgroundColor: '#000000ff',
                    color: '#ffffffff',
                    fontSize: 16,
                    roundingValue: 0,
                    roundingPercentage: 0,
                    showPercentage: true,
                    showValue: true
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
                    showValue: true,
                    showPercentage: true,
                    roundingValue: 0,
                    roundingPercentage: 0
                },
                title: {
                    text: 'Performance by Subjects',
                    color: '#ffffffff',
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
                }
            }
        }
    });

const dataset = ref([
    {
        name: 'series 1',
        values: [
            100
        ],
        color: '#1f77b4'
    },
    {
        name: 'series 2',
        values: [
            50
        ],
        color: '#aec7e8'
    },
    {
        name: 'series 3',
        values: [
            25
        ],
        color: '#ff7f0e'
    },
    {
        name: 'name',
        values: [],
        color: '#42d392'
    },
    {
        name: 'name',
        values: [],
        color: '#42d392'
    },
    {
        name: 'name',
        values: [],
        color: '#42d392'
    },
    {
        name: 'name',
        values: [],
        color: '#42d392'
    }
]);

</script>
<template>
    <!-- Using a wrapper is optional -->
    <div :style="{ width: '600px'}">
        <VueUiDonut
            :config="config"
            :dataset="dataset"
        />
    </div>
</template>