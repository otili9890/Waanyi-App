import React, { Component, useState } from "react";
import { StyleSheet, Text, View, FlatList, Button } from "react-native";
import { Overlay } from "react-native-elements";

export default function ItemOverlay (item: any, onBackdropPress: Function) {

  console.log(item.id);

  return (
    <Overlay isVisible={true} onBackdropPress={() => onBackdropPress()} >
      <Text>{item.id}</Text>
      <Text>Part of speech: {item.Part_of_Speech}</Text>
      <Text>English_Gloss: {item.English_Gloss}</Text>
      <Text>Definition: {item.Definition}</Text>
      <Text>JFejewjf</Text>
      <Button onPress={() => onBackdropPress()} title="Exit" />
    </Overlay>
      
  );
}

const styles = StyleSheet.create({
  
});