import React, { Component, useState } from "react";
import { StyleSheet, Text, View, FlatList, Button } from "react-native";
import { Overlay } from "react-native-elements";

export default function ItemOverlay (item: any) {
  const [visible, setVisible] = useState(true);

  const toggleOverlay = () => {
    setVisible(!visible);
  };

  console.log(item.id);

  return (
    <Overlay isVisible={visible} onBackdropPress={toggleOverlay} >
      <Text>{item.id}</Text>
      <Text>Part of speech: {item.Part_of_Speech}</Text>
      <Text>English_Gloss: {item.English_Gloss}</Text>
      <Text>Definition: {item.Definition}</Text>
      <Text>JFejewjf</Text>
      <Button onPress={toggleOverlay} title="Exit" />
    </Overlay>
      
  );
}

const styles = StyleSheet.create({
  
});