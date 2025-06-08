import React, { useRef, useEffect, useState } from 'react';
import * as d3 from 'd3';

const D3PriceChart = ({ prices, news, onMarkerHover, onMarkerLeave }) => {
  const chartRef = useRef();
  const [dimensions, setDimensions] = useState({ width: 0, height: 450 });

  // Функция для поиска ближайшей точки на графике для каждой новости
  const mapNewsToPricePoints = (prices, news) => {
    if (!prices || prices.length === 0 || !news || news.length === 0) return [];
    
    return news.map(newsItem => {
      const newsTimestamp = new Date(newsItem.news_date).getTime();
      let closestPoint = null;
      let minDiff = Infinity;

      prices.forEach(p => {
        const diff = Math.abs((p[0] * 1000) - newsTimestamp); // Сравниваем мс с мс
        if (diff < minDiff) {
          minDiff = diff;
          closestPoint = p;
        }
      });
      
      // chartX по-прежнему в секундах, конвертируем при использовании
      return { ...newsItem, chartX: closestPoint[0], chartY: closestPoint[1] };
    });
  };

  useEffect(() => {
    // Определяем размеры контейнера для адаптивности
    const resizeObserver = new ResizeObserver(entries => {
      if (entries && entries.length > 0) {
        const { width } = entries[0].contentRect;
        setDimensions({ width, height: 450 });
      }
    });
    resizeObserver.observe(chartRef.current.parentNode);
    return () => resizeObserver.disconnect();
  }, []);

  useEffect(() => {
    if (!prices || prices.length === 0 || dimensions.width === 0) return;

    const margin = { top: 20, right: 30, bottom: 40, left: 70 };
    const width = dimensions.width - margin.left - margin.right;
    const height = dimensions.height - margin.top - margin.bottom;
    
    // Очищаем SVG перед перерисовкой
    const svg = d3.select(chartRef.current);
    svg.selectAll("*").remove();
    
    const chart = svg.append("g")
      .attr("transform", `translate(${margin.left}, ${margin.top})`);
      
    // Определяем оси, конвертируя секунды в мс для домена
    const xScale = d3.scaleTime()
      .domain(d3.extent(prices, d => d[0] * 1000))
      .range([0, width]);
      
    const yScale = d3.scaleLinear()
      .domain([d3.min(prices, d => d[1]) * 0.95, d3.max(prices, d => d[1]) * 1.05])
      .range([height, 0]);
      
    // Рисуем оси
    const xAxis = d3.axisBottom(xScale).tickFormat(d3.timeFormat("%d.%m.%Y"));
    chart.append("g")
      .attr("class", "axis-x")
      .attr("transform", `translate(0, ${height})`)
      .call(xAxis)
      .selectAll("text")
        .style("fill", "#A6A6A6")
        .attr("transform", "rotate(-45)")
        .style("text-anchor", "end");
        
    const yAxis = d3.axisLeft(yScale).tickFormat(d => `₽${d.toFixed(2)}`);
    chart.append("g")
      .attr("class", "axis-y")
      .call(yAxis)
      .selectAll("text")
        .style("fill", "#A6A6A6");

    // Стилизация осей
    chart.selectAll(".domain").attr("stroke", "#404040");
    chart.selectAll(".tick line").attr("stroke", "#404040");

    // Рисуем линию цены, конвертируя секунды в мс
    const lineGenerator = d3.line()
      .x(d => xScale(d[0] * 1000))
      .y(d => yScale(d[1]))
      .curve(d3.curveMonotoneX);
      
    chart.append("path")
      .datum(prices)
      .attr("fill", "none")
      .attr("stroke", "#FFDD2D")
      .attr("stroke-width", 2.5)
      .attr("d", lineGenerator);

    // Подготавливаем и рисуем маркеры новостей
    const newsPoints = mapNewsToPricePoints(prices, news);
    
    chart.selectAll(".news-marker")
      .data(newsPoints)
      .enter()
      .append("g")
      .attr("class", "news-marker-group")
      // Конвертируем секунды в мс при позиционировании
      .attr("transform", d => `translate(${xScale(d.chartX * 1000)}, ${yScale(d.chartY)})`)
      .on('mouseenter', (event, d) => {
        d3.select(event.currentTarget).select('text').transition().duration(200).attr('font-size', '24px');
        onMarkerHover(d, { top: event.pageY, left: event.pageX });
      })
      .on('mouseleave', (event, d) => {
        d3.select(event.currentTarget).select('text').transition().duration(200).attr('font-size', '18px');
        onMarkerLeave();
      })
      .each(function(d) {
        const g = d3.select(this);

        g.append('line')
          .attr('x1', 0)
          .attr('y1', 0)
          .attr('x2', 0)
          .attr('y2', height - yScale(d.chartY))
          .attr('stroke', '#A6A6A6')
          .attr('stroke-width', 1)
          .attr('stroke-dasharray', '3,3');
        
        g.append('text')
          .attr('text-anchor', 'middle')
          .attr('y', -10)
          .attr('font-size', '18px')
          .style('cursor', 'pointer')
          .style('fill', '#FFDD2D')
          .text('🔔');
      });

  }, [prices, news, dimensions, onMarkerHover, onMarkerLeave]);

  return <svg ref={chartRef} width="100%" height={dimensions.height}></svg>;
};

export default D3PriceChart;